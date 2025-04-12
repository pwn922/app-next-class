import uuid
import logging
from flask_restful import Resource, request
from flasgger.utils import swag_from
from database.db import db
from models.user import User
from utils.responses import success_response, error_response
from responses.user_response import UserSuccessResponse, UserErrorResponse

logging.basicConfig(level=logging.INFO)


class UserResource(Resource):
    @swag_from('../docs/users/get.yml')
    def get(self, user_id):
        try:
            user = db.session.query(User).filter_by(id=user_id).first()
            if not user:
                return error_response(
                    error_code=UserErrorResponse.NOT_FOUND.name,
                    status_code=UserErrorResponse.NOT_FOUND.value
                    .get("status_code"),
                    message=UserErrorResponse.NOT_FOUND.value
                    .get("message")
                )

            user_obj = {
                "id": str(user.id),
                "name": user.name,
                "email": user.email
            }
            return success_response(
                message_key=UserSuccessResponse.RETRIEVED.value
                .get("message"),
                status_code=UserSuccessResponse.RETRIEVED.value
                .get("status_code"),
                data=user_obj
            )
        except Exception as e:
            logging.error(f"Unexpected error during get user: {e}")
            return error_response(
                error_code=UserErrorResponse.UNEXPECTED_ERROR.name,
                status_code=UserErrorResponse.UNEXPECTED_ERROR.value
                .get("status_code"),
                message=UserErrorResponse.UNEXPECTED_ERROR.value
                .get("message")
            )

    @swag_from('../docs/users/put.yml')
    def put(self, user_id):
        try:
            user = db.session.query(User).filter_by(id=user_id).first()
            if not user:
                return error_response(
                    error_code=UserErrorResponse.NOT_FOUND.name,
                    status_code=UserErrorResponse.NOT_FOUND.value
                    .get("status_code"),
                    message=UserErrorResponse.NOT_FOUND.value
                    .get("message")
                )

            data = request.json
            user.name = data.get("name", user.name)
            user.email = data.get("email", user.email)

            db.session.commit()

            return success_response(
                message_key=UserSuccessResponse.UPDATED.value
                .get("message"),
                status_code=UserSuccessResponse.UPDATED.value
                .get("status_code"),
                data={
                    "id": str(user.id),
                    "name": user.name,
                    "email": user.email
                }
            )
        except Exception as e:
            logging.error(f"Unexpected error during put user: {e}")
            return error_response(
                error_code=UserErrorResponse.UNEXPECTED_ERROR.name,
                status_code=UserErrorResponse.UNEXPECTED_ERROR.value
                .get("status_code"),
                message=UserErrorResponse.UNEXPECTED_ERROR.value
                .get("message")
            )

    @swag_from('../docs/users/delete.yml')
    def delete(self, user_id):
        try:
            user = db.session.query(User).filter_by(id=user_id).first()
            if not user:
                return error_response(
                    error_code=UserErrorResponse.NOT_FOUND.name,
                    status_code=UserErrorResponse.NOT_FOUND.value
                    .get("status_code"),
                    message=UserErrorResponse.NOT_FOUND.value
                    .get("message")
                )

            db.session.delete(user)
            db.session.commit()

            return success_response(
                message_key=UserSuccessResponse.DELETED.value
                .get("message"),
                status_code=UserSuccessResponse.DELETED.value
                .get("status_code")
            )
        except Exception as e:
            logging.error(f"Unexpected error during delete user: {e}")
            return error_response(
                error_code=UserErrorResponse.UNEXPECTED_ERROR.name,
                status_code=UserErrorResponse.UNEXPECTED_ERROR.value
                .get("status_code"),
                message=UserErrorResponse.UNEXPECTED_ERROR.value
                .get("message")
            )


class UserListResource(Resource):
    @swag_from("../docs/users/get_all.yml")
    def get(self):
        try:
            users = db.session.query(User).all()
            result = [
                {"id": str(user.id), "name": user.name, "email": user.email}
                for user in users
            ]
            return success_response(
                message_key=UserSuccessResponse.LIST_RETRIEVED.value
                .get("message"),
                status_code=UserSuccessResponse.LIST_RETRIEVED.value
                .get("status_code"),
                data=result
            )
        except Exception as e:
            logging.error(f"Unexpected error during get users: {e}")
            return error_response(
                error_code=UserErrorResponse.UNEXPECTED_ERROR.name,
                status_code=UserErrorResponse.UNEXPECTED_ERROR.value
                .get("status_code"),
                message=UserErrorResponse.UNEXPECTED_ERROR.value
                .get("message")
            )

    @swag_from("../docs/users/post.yml")
    def post(self):
        try:
            data = request.json
            name = data.get("name")
            email = data.get("email")
            password = data.get("password")

            if not name or not email or not password:
                return error_response(
                    error_code=UserErrorResponse.MISSING_FIELDS.name,
                    status_code=UserErrorResponse.MISSING_FIELDS.value
                    .get("status_code"),
                    message=UserErrorResponse.MISSING_FIELDS.value
                    .get("message")
                )

            new_user = User(
                id=uuid.uuid4(),
                name=name,
                email=email,
                password=password
            )

            db.session.add(new_user)
            db.session.commit()

            return success_response(
                message_key=UserSuccessResponse.CREATED.value
                .get("message"),
                status_code=UserSuccessResponse.CREATED.value
                .get("status_code"),
                data={
                    "id": str(new_user.id),
                    "name": new_user.name,
                    "email": new_user.email
                }
            )
        except Exception as e:
            logging.error(f"Unexpected error during post users: {e}")
            return error_response(
                error_code=UserErrorResponse.UNEXPECTED_ERROR.name,
                status_code=UserErrorResponse.UNEXPECTED_ERROR.value
                .get("status_code"),
                message=UserErrorResponse.UNEXPECTED_ERROR.value
                .get("message")
            )
