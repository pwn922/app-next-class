from datetime import datetime, timedelta, timezone
# import uuid
import logging

from flask import request, redirect, session
from flask_restful import Resource
from flask_jwt_extended import create_access_token, create_refresh_token
from flasgger.utils import swag_from

from oauthlib.oauth2.rfc6749.errors import OAuth2Error

from responses.login_response import (
    LoginErrorResponse,
    LoginSuccessResponse
)

from utils.responses import error_response, success_response

from exceptions.oauth2 import (
    OAuth2ExternalServiceError,
    OAuth2FlowError,
)

from database.db import db
from models.user import User
from auth import oauth2


logging.basicConfig(level=logging.INFO)

OAUTH_STATE_SESSION = "oauth_state"


class LoginResource(Resource):
    @swag_from('../docs/login/get.yml')
    def get(self):
        try:
            return self.start_oauth_flow()

        except OAuth2Error as oauth_err:
            logging.error(f"OAuth2 error: {oauth_err}")
            return error_response(
                error_code=LoginErrorResponse.OAUTH2_ERROR.name,
                status_code=LoginErrorResponse.OAUTH2_ERROR.value
                .get("status_code"),
                message=LoginErrorResponse.OAUTH2_ERROR.value
                .get("message"),
            )

        except OAuth2ExternalServiceError as ex_err:
            logging.error(f"External service error: {ex_err}")
            return error_response(
                error_code=LoginErrorResponse.EXTERNAL_SERVICE_ERROR.name,
                status_code=LoginErrorResponse.EXTERNAL_SERVICE_ERROR.value
                .get("status_code"),
                message=LoginErrorResponse.EXTERNAL_SERVICE_ERROR
                .value.get("message"),
            )

        except Exception as e:
            logging.exception(f"Unexpected error during login process: {e}")
            return error_response(
                error_code=LoginErrorResponse.UNEXPECTED_ERROR.name,
                status_code=LoginErrorResponse.UNEXPECTED_ERROR.value
                .get("status_code"),
                message=LoginErrorResponse.UNEXPECTED_ERROR
                .value.get("message"),
            )

    def start_oauth_flow(self):
        openid_conf = self._get_openid_configuration()
        authorization_url, state = self._generate_authorization_url(
            openid_conf
        )
        session[OAUTH_STATE_SESSION] = state
        logging.info("Authorization URL generated")
        return redirect(authorization_url, 302)

    def _get_openid_configuration(self):
        openid_conf = oauth2.get_openid_configuration()
        if not isinstance(openid_conf, dict) or not openid_conf:
            raise OAuth2ExternalServiceError(
                "Unable to fetch or invalid OpenID configuration from Google.",
                "INVALID_OPENID_CONF"
            )
        return openid_conf

    def _generate_authorization_url(self, openid_conf):
        authorization_endpoint = openid_conf.get("authorization_endpoint")
        if not authorization_endpoint:
            raise OAuth2ExternalServiceError(
                "Authorization endpoint not found in OpenID configuration.",
                "MISSING_AUTH_ENDPOINT"
            )
        oauth_session = oauth2.create_oauth2_session()
        return oauth_session.authorization_url(
            authorization_endpoint,
            access_type="offline",
            prompt="consent"
        )


class LoginCallbackResource(Resource):
    def get(self):
        try:
            state = request.args.get("state", "")
            if not self._is_state_valid(state):
                logging.error(f"Invalid State: {state}")
                return error_response(
                    error_code=LoginErrorResponse.INVALID_STATE.name,
                    status_code=LoginErrorResponse.INVALID_STATE.value
                    .get("status_code"),
                    message=LoginErrorResponse.INVALID_STATE
                    .value.get("message"),
                )

            token = self._fetch_oauth_token(request.url, state)
            logging.info(f"Fetched Token: {token}")
            user_info = self._verify_and_get_user_info(token)
            jwt_token = self._generate_jwt(user_info)

            session.pop(OAUTH_STATE_SESSION, None)

            return success_response(
                message_key=LoginSuccessResponse.LOGIN_SUCCESS.value
                .get("message"),
                status_code=LoginSuccessResponse.LOGIN_SUCCESS.value
                .get("status_code"),
                data={"token": jwt_token},
            )

        except OAuth2FlowError as oe:
            logging.error(f"OAuth Flow Error: {oe}")
            return error_response(
                error_code=LoginErrorResponse.OAUTH2_FLOW_ERROR.name,
                status_code=LoginErrorResponse.OAUTH2_FLOW_ERROR.value
                .get("status_code"),
                message=LoginErrorResponse.OAUTH2_FLOW_ERROR
                .value.get("message")
            )

        except OAuth2Error as oauth_err:
            logging.error(f"OAuth2 Error: {oauth_err}")
            return error_response(
                error_code=LoginErrorResponse.OAUTH2_ERROR.name,
                status_code=LoginErrorResponse.OAUTH2_ERROR.value
                .get("status_code"),
                message=LoginErrorResponse.OAUTH2_ERROR.value.get("message")
            )

        except Exception as e:
            logging.exception(f"Unexpected error during login callback: {e}")
            return error_response(
                error_code=LoginErrorResponse.UNEXPECTED_ERROR.name,
                status_code=LoginErrorResponse.UNEXPECTED_ERROR.value
                .get("status_code"),
                message=LoginErrorResponse.UNEXPECTED_ERROR
                .value.get("message")
            )

    def _is_state_valid(self, state):
        oauth_state = session.get(OAUTH_STATE_SESSION, "")
        return state and oauth_state and state == oauth_state

    def _fetch_oauth_token(self, authorization_response, state):
        oauth_session = oauth2.create_oauth2_session(state)
        openid_conf = oauth2.get_openid_configuration()
        token_url = openid_conf.get("token_endpoint")
        if not token_url:
            raise OAuth2FlowError(
                "Token endpoint not found in OpenID configuration.",
                "MISSING_TOKEN_ENDPOINT"
            )

        return oauth_session.fetch_token(
            token_url,
            authorization_response=authorization_response,
            client_secret=oauth2.CLIENT_SECRET
        )

    def _verify_and_get_user_info(self, token):
        id_token = token.get("id_token")
        if not id_token:
            raise OAuth2Error("Invalid token.", "INVALID_ID_TOKEN")

        user_info = oauth2.verify_id_token(id_token)
        if not user_info:
            raise OAuth2Error("Failed to verify ID token.")

        return user_info

    def _generate_jwt(self, user_info):
        sub = user_info.get("sub")
        email = user_info.get("email")
        exp = user_info.get('exp')

        user = db.session.query(User).filter_by(oidc_sub=sub).first()
        if not user:
            user = User(oidc_sub=sub, email=email)
            db.session.add(user)
            db.session.commit()

        logging.info(f"User: {user}")

        identity = user.oidc_sub
        expire_datetime = datetime.fromtimestamp(exp, tz=timezone.utc)
        expires_delta = expire_datetime - datetime.now(timezone.utc)
        expires_delta_refresh = timedelta(days=7)

        logging.info(f"Access token will expire in: {expires_delta}")
        logging.info(f"Refresh token will expire in: {expires_delta_refresh}")

        jwt_token = create_access_token(
            identity=identity,
            expires_delta=expires_delta
        )

        jwt_refresh_token = create_refresh_token(
            identity=identity,
            expires_delta=expires_delta_refresh
        )

        logging.info(f"Refresh token: {jwt_refresh_token}")
        return jwt_token
