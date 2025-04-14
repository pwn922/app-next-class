# register.py

import logging

from flask import request
from flask_restful import Resource
from utils.security import generate_password_hash

from responses.register_response import (
    RegisterErrorResponse,
    RegisterSuccessResponse
)
from utils.responses import error_response, success_response

from database.db import db
from models.user import User

logging.basicConfig(level=logging.INFO)


class RegisterResource(Resource):
    def post(self):
        try:
            data = request.get_json()
            email = data.get("email")
            password = data.get("password")

            if not email or not password:
                return error_response(
                    error_code=RegisterErrorResponse.MISSING_CREDENTIALS.name,
                    status_code=RegisterErrorResponse.MISSING_CREDENTIALS.value
                    .get("status_code"),
                    message=RegisterErrorResponse.MISSING_CREDENTIALS.value
                    .get("message")
                )

            if db.session.query(User).filter_by(email=email).first():
                return error_response(
                    error_code=RegisterErrorResponse.EMAIL_ALREADY_EXISTS.name,
                    status_code=RegisterErrorResponse.EMAIL_ALREADY_EXISTS
                    .value.get("status_code"),
                    message=RegisterErrorResponse.EMAIL_ALREADY_EXISTS.value
                    .get("message")
                )

            hashed_password = generate_password_hash(password)
            new_user = User(email=email, password=hashed_password)
            db.session.add(new_user)
            db.session.commit()

            return success_response(
                message_key=RegisterSuccessResponse.REGISTRATION_SUCCESS.value
                .get("message"),
                status_code=RegisterSuccessResponse.REGISTRATION_SUCCESS.value
                .get("status_code"),
                data={"email": new_user.email}
            )

        except Exception as e:
            logging.exception(f"Error during registration: {e}")
            return error_response(
                error_code=RegisterErrorResponse.UNEXPECTED_ERROR.name,
                status_code=RegisterErrorResponse.UNEXPECTED_ERROR.value
                .get("status_code"),
                message=RegisterErrorResponse.UNEXPECTED_ERROR.value
                .get("message")
            )
