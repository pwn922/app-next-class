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
    def get(self, id):
        try:
            user = db.session.query(User).filter_by(id=id).first()
            if not user:
                return error_response(
                    error_code=UserErrorResponse.NOT_FOUND.name,
                    status_code=UserErrorResponse.NOT_FOUND.value.get("status_code"),
                    message=UserErrorResponse.NOT_FOUND.value.get("message")
                )

            user_obj = {
                "id": user.id,
                "email": user.email,
                "created_at": user.created_at.isoformat()
            }
            return success_response(
                message_key=UserSuccessResponse.RETRIEVED.value.get("message"),
                status_code=UserSuccessResponse.RETRIEVED.value.get("status_code"),
                data=user_obj
            )
        except Exception as e:
            logging.error(f"Unexpected error during get user: {e}")
            return error_response(
                error_code=UserErrorResponse.UNEXPECTED_ERROR.name,
                status_code=UserErrorResponse.UNEXPECTED_ERROR.value.get("status_code"),
                message=UserErrorResponse.UNEXPECTED_ERROR.value.get("message")
            )

    @swag_from('../docs/users/put.yml')
    def put(self, id):
        try:
            user = db.session.query(User).filter_by(id=id).first()
            if not user:
                return error_response(
                    error_code=UserErrorResponse.NOT_FOUND.name,
                    status_code=UserErrorResponse.NOT_FOUND.value.get("status_code"),
                    message=UserErrorResponse.NOT_FOUND.value.get("message")
                )

            data = request.json
            user.email = data.get("email", user.email)

            db.session.commit()

            return success_response(
                message_key=UserSuccessResponse.UPDATED.value.get("message"),
                status_code=UserSuccessResponse.UPDATED.value.get("status_code"),
                data={
                    "id": user.id,
                    "email": user.email,
                    "created_at": user.created_at.isoformat()
                }
            )
        except Exception as e:
            logging.error(f"Unexpected error during put user: {e}")
            return error_response(
                error_code=UserErrorResponse.UNEXPECTED_ERROR.name,
                status_code=UserErrorResponse.UNEXPECTED_ERROR.value.get("status_code"),
                message=UserErrorResponse.UNEXPECTED_ERROR.value.get("message")
            )

    @swag_from('../docs/users/delete.yml')
    def delete(self, id):
        try:
            user = db.session.query(User).filter_by(id=id).first()
            if not user:
                return error_response(
                    error_code=UserErrorResponse.NOT_FOUND.name,
                    status_code=UserErrorResponse.NOT_FOUND.value.get("status_code"),
                    message=UserErrorResponse.NOT_FOUND.value.get("message")
                )

            db.session.delete(user)
            db.session.commit()

            return success_response(
                message_key=UserSuccessResponse.DELETED.value.get("message"),
                status_code=UserSuccessResponse.DELETED.value.get("status_code")
            )
        except Exception as e:
            logging.error(f"Unexpected error during delete user: {e}")
            return error_response(
                error_code=UserErrorResponse.UNEXPECTED_ERROR.name,
                status_code=UserErrorResponse.UNEXPECTED_ERROR.value.get("status_code"),
                message=UserErrorResponse.UNEXPECTED_ERROR.value.get("message")
            )


class UserListResource(Resource):
    @swag_from("../docs/users/get_all.yml")
    def get(self):
        try:
            users = db.session.query(User).all()
            result = [
                {
                    "id": user.id,
                    "email": user.email,
                    "created_at": user.created_at.isoformat()
                }
                for user in users
            ]
            return success_response(
                message_key=UserSuccessResponse.LIST_RETRIEVED.value.get("message"),
                status_code=UserSuccessResponse.LIST_RETRIEVED.value.get("status_code"),
                data=result
            )
        except Exception as e:
            logging.error(f"Unexpected error during get users: {e}")
            return error_response(
                error_code=UserErrorResponse.UNEXPECTED_ERROR.name,
                status_code=UserErrorResponse.UNEXPECTED_ERROR.value.get("status_code"),
                message=UserErrorResponse.UNEXPECTED_ERROR.value.get("message")
            )

    @swag_from("../docs/users/post.yml")
    def post(self):
        try:
            data = request.json
            id = data.get("id")
            email = data.get("email")

            if not id or not email:
                return error_response(
                    error_code=UserErrorResponse.MISSING_FIELDS.name,
                    status_code=UserErrorResponse.MISSING_FIELDS.value.get("status_code"),
                    message=UserErrorResponse.MISSING_FIELDS.value.get("message")
                )

            new_user = User(
                id=id,
                email=email
            )

            db.session.add(new_user)
            db.session.commit()

            return success_response(
                message_key=UserSuccessResponse.CREATED.value.get("message"),
                status_code=UserSuccessResponse.CREATED.value.get("status_code"),
                data={
                    "id": new_user.id,
                    "email": new_user.email,
                    "created_at": new_user.created_at.isoformat()
                }
            )
        except Exception as e:
            logging.error(f"Unexpected error during post user: {e}")
            return error_response(
                error_code=UserErrorResponse.UNEXPECTED_ERROR.name,
                status_code=UserErrorResponse.UNEXPECTED_ERROR.value.get("status_code"),
                message=UserErrorResponse.UNEXPECTED_ERROR.value.get("message")
            )
