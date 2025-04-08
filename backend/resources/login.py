from datetime import datetime
from datetime import timedelta
from datetime import timezone

import uuid

import jwt
from jwt.exceptions import InvalidAlgorithmError
#from flasgger.utils import swag_from
from database.db import db
from models.user import User
from models.refresh_token import RefreshToken
from flask import request, jsonify, redirect, session, make_response
import logging
from flask_restful import Resource
from oauthlib.oauth2.rfc6749.errors import InvalidGrantError, InsecureTransportError, OAuth2Error
from auth import oauth2
from flask_jwt_extended import create_access_token, create_refresh_token #, verify_jwt_in_request, get_jwt_identity

#from flask_jwt_extended.exceptions import RevokedTokenError


logging.basicConfig(level=logging.INFO)

OAUTH_STATE_SESSION = "oauth_state"

AUTH_ERROR = {"success": False, "message": "An error has occurred in the authentication process.", "error_code": "AUTH_ERROR", "data": {}}
ALREADY_LOGGED_IN = {"success": True, "message": "You are still logged in.", "data": {}}
LOGIN_SUCCESS = {"success": True, "message": "Login successful.", "data": {}}

INVALID_JWT = {"success": False, "message": "The JWT provided is not valid.", "error_code": "INVALID_JWT", "data": {}}


# TODO - MEJORAR LOS ERRORES Y LOS ARRIBA
# TODO - CREAR REFRESH TOKEN ENDPOINT
# TODO - ALMACENAR O ACTUALIZAR EL REFRESH TOKEN
# TODO - CREAR CERRAR SESIÓN Y ELIMINAR ACCESS_TOKEN y EL DE GOOGLE. 
# TODO - PREGUNTAR SI DEBERIA ALMACENAR EL REFRESH TOKEN. 
# TODO - COLOCAR EXP DEL GOOGLE ID_TOKEN EN MI ACESS_TOKEN.
# TODO - MEJORAR LOS CODIGO DE ESTADOS EN LoginCallbackResource


class LoginResource(Resource):
    def get(self):
        try:
            return self.start_oauth_flow()

        except InvalidAlgorithmError as iae:
            logging.error(f"InvalidAlgorithmError: {iae}")
            return make_response(jsonify(INVALID_JWT), 401)
        except (Exception, ValueError, OAuth2Error) as e:
            logging.exception(f"Error during login process: {e}\n")
            return make_response(jsonify(AUTH_ERROR), 500)

    def start_oauth_flow(self):
        openid_conf = self._get_openid_configuration()
        authorization_url, state = self._generate_authorization_url(openid_conf)

        session[OAUTH_STATE_SESSION] = state
        logging.info(f"Authorization URL generated: {authorization_url}")

        return redirect(authorization_url, 302)

    def _get_openid_configuration(self):
        openid_conf = oauth2.get_openid_configuration()

        if not openid_conf:
            raise ValueError("Invalid OpenID config.")

        logging.info(f"OAuth2 Configuration: {openid_conf}")
        return openid_conf

    def _generate_authorization_url(self, openid_conf):
        authorization_endpoint = openid_conf.get("authorization_endpoint")

        if not authorization_endpoint:
            raise ValueError("Authorization endpoint not found in OpenID configuration.")

        oauth_session = oauth2.create_oauth2_session()
        authorization_url, state = oauth_session.authorization_url(
            authorization_endpoint,
            access_type="offline",
            prompt="consent"
        )
        return authorization_url, state

class LoginCallbackResource(Resource):
    def get(self):
        try:
            state = request.args.get("state", "")
            if not self._is_state_valid(state):
                logging.error(f"Invalid State: {state}")
                return make_response(jsonify(AUTH_ERROR), 400)

            token = self._fetch_oauth_token(request.url, state)
            logging.info(f"Fetch Token: {token}\n")

            user_info = self._verify_and_get_user_info(token)
            jwt_token = self._generate_jwt(user_info)

            session.pop(OAUTH_STATE_SESSION, None)
            return make_response(jsonify({**LOGIN_SUCCESS, "data": {"token": jwt_token}}), 200)
        except InvalidGrantError as ige:
            logging.error(f"InvalidGrantError: {ige}")
            return make_response(jsonify(AUTH_ERROR), 400)
        except ValueError as ve:
            logging.error(f"Value Error: {ve}")
            return make_response(jsonify(AUTH_ERROR), 400)
        except jwt.PyJWTError as je:
            logging.error(f"JWT Error: {je}")
            return make_response(jsonify(AUTH_ERROR), 400)
        except InsecureTransportError as ite:
            logging.error(f"InsecureTransportError: {ite}")
            return make_response(jsonify(AUTH_ERROR), 400)    
        except Exception as e:
            logging.exception(f"Error during login callback: {e}")
            return make_response(jsonify(AUTH_ERROR), 500)

    def _is_state_valid(self, state):
        oauth_state = session.get(OAUTH_STATE_SESSION, "")
        return state and oauth_state and state == oauth_state

    def _fetch_oauth_token(self, authorization_response, state):
        oauth_session = oauth2.create_oauth2_session(state)
        openid_conf = oauth2.get_openid_configuration()
        token_url = openid_conf.get("token_endpoint")

        if not token_url:
            raise ValueError("Token endpoint not found in OpenID configuration.")

        token = oauth_session.fetch_token(
            token_url,
            authorization_response=authorization_response,
            client_secret=oauth2.CLIENT_SECRET
        )
        return token

    def _verify_and_get_user_info(self, token):
        id_token = token.get("id_token")
        if not id_token:
            raise ValueError("Invalid token.")

        user_info = oauth2.verify_id_token(id_token)
        if not user_info:
            raise jwt.PyJWTError("Failed to verify ID token.")
        return user_info

    def _generate_jwt(self, user_info):
        sub = user_info.get("sub")
        email = user_info.get("email")
        exp = user_info.get('exp')
        user = db.session.query(User).filter_by(google_id=sub).first()
        if not user:
            user = User(id=uuid.uuid4(), google_id=sub, email=email)
            db.session.add(user)
            db.session.commit()
        
        logging.info(f"User: {user}")

        identity = user.google_id

        expire_datetime = datetime.fromtimestamp(exp, tz=timezone.utc)
        expires_delta = expire_datetime - datetime.now(timezone.utc)

        expires_delta_refresh = timedelta(days=7)

        logging.info(f"Access token will expire on: {expires_delta} (hh:mm:ss)")

        logging.info(f"Refresh token will expire on: {expires_delta_refresh} (days)")

        jwt_token = create_access_token(
            identity=identity, 
            expires_delta=expires_delta)
        
        jwt_refresh_token = create_refresh_token(
            identity=identity, 
            expires_delta=expires_delta_refresh
        )

        logging.info(f"Refresh token: {jwt_refresh_token}")

        return jwt_token