from datetime import timedelta
import logging

from flask import request
from flask_restful import Resource
from flask_jwt_extended import create_access_token, create_refresh_token
from flasgger.utils import swag_from
from utils.security import verify_password
from responses.login_response import LoginErrorResponse, LoginSuccessResponse
from utils.responses import error_response, success_response

from database.db import db
from models.user import User

logging.basicConfig(level=logging.INFO)


class LoginResource(Resource):
    @swag_from('../docs/login/post.yml')
    def post(self):
        try:
            data = request.get_json()
            email = data.get("email")
            password = data.get("password")

            if not email or not password:
                return error_response(
                    error_code=LoginErrorResponse.INVALID_CREDENTIALS.name,
                    status_code=LoginErrorResponse.INVALID_CREDENTIALS.value
                    .get("status_code"),
                    message=LoginErrorResponse.INVALID_CREDENTIALS.value
                    .get("message")
                )

            user = db.session.query(User).filter_by(email=email).first()
            
            if not user or not verify_password(
                user.password,
                password
                
            ):
                return error_response(
                    error_code=LoginErrorResponse.INVALID_CREDENTIALS.name,
                    status_code=LoginErrorResponse.INVALID_CREDENTIALS.value
                    .get("status_code"),
                    message=LoginErrorResponse.INVALID_CREDENTIALS.value
                    .get("message")
                )

            identity = user.id
            access_token_expires = timedelta(hours=1)
            refresh_token_expires = timedelta(days=7)
            access_token = create_access_token(
                identity=identity,
                expires_delta=access_token_expires
            )
            refresh_token = create_refresh_token(
                identity=identity,
                expires_delta=refresh_token_expires
            )

            return success_response(
                message_key=LoginSuccessResponse.LOGIN_SUCCESS.value
                .get("message"),
                status_code=LoginSuccessResponse.LOGIN_SUCCESS.value
                .get("status_code"),
                data={
                    "access_token": access_token,
                    "refresh_token": refresh_token
                }
            )
        except Exception as e:
            logging.exception(f"Error during manual login: {e}")
            return error_response(
                error_code=LoginErrorResponse.UNEXPECTED_ERROR.name,
                status_code=LoginErrorResponse.UNEXPECTED_ERROR.value
                .get("status_code"),
                message=LoginErrorResponse.UNEXPECTED_ERROR.value
                .get("message")
            )
