"""
from flask import request
import logging
from flask_restful import Resource
from flasgger import swag_from
import uuid
from database.db import db
from models.classroom import Classroom
from utils.responses import success_response, error_response
from responses.classroom_response import (
    ClassroomErrorResponse,
    ClassroomSuccessResponse
)

logging.basicConfig(level=logging.INFO)


class ClassroomResource(Resource):
    @swag_from('../docs/classrooms/get.yml')
    def get(self, id):
        try:
            classroom = db.session.query(Classroom).filter_by(id=id).first()
            if not classroom:
                return error_response(
                    error_code=ClassroomErrorResponse.NOT_FOUND.name,
                    status_code=ClassroomErrorResponse.NOT_FOUND.value
                    .get("status_code"),
                    message=ClassroomErrorResponse.NOT_FOUND.value
                    .get("message")
                )

            classroom_data = {
                "id": classroom.id,
                "number": classroom.number,
                "pavilion_id": classroom.pavilion_id
            }
            return success_response(
                message_key=ClassroomSuccessResponse.RETRIEVED.value
                .get("message"),
                status_code=ClassroomSuccessResponse.RETRIEVED.value
                .get("status_code"),
                data=classroom_data
            )
        except Exception as e:
            logging.error(f"Unexpected error: {e}")
            return error_response(
                error_code=ClassroomErrorResponse.UNEXPECTED_ERROR.name,
                status_code=ClassroomErrorResponse.UNEXPECTED_ERROR.value,
                message=ClassroomErrorResponse.UNEXPECTED_ERROR.value
                .get("message"),
            )

    @swag_from('../docs/classrooms/put.yml')
    def put(self, id):
        try:
            classroom = db.session.query(Classroom).filter_by(id=id).first()
            if not classroom:
                return error_response(
                    error_code=ClassroomErrorResponse.NOT_FOUND.name,
                    status_code=ClassroomErrorResponse.NOT_FOUND.value
                    .get("status_code"),
                    message=ClassroomErrorResponse.NOT_FOUND.value
                    .get("message")
                )

            data = request.json
            classroom.number = data.get("number", classroom.number)
            classroom.pavilion_id = data.get(
                "pavilion_id",
                classroom.pavilion_id
            )

            db.session.commit()

            updated = {
                "id": classroom.id,
                "number": classroom.number,
                "pavilion_id": classroom.pavilion_id
            }
            return success_response(
                message_key=ClassroomSuccessResponse.UPDATED.value
                .get("message"),
                status_code=ClassroomSuccessResponse.UPDATED.value
                .get("status_code"),
                data=updated
            )
        except Exception as e:
            logging.error(f"Unexpected error: {e}")
            return error_response(
                error_code=ClassroomErrorResponse.UNEXPECTED_ERROR.name,
                status_code=ClassroomErrorResponse.UNEXPECTED_ERROR.value
                .get("status_code"),
                message=ClassroomErrorResponse.UNEXPECTED_ERROR.value
                .get("message")
            )

    @swag_from('../docs/classrooms/delete.yml')
    def delete(self, id):
        try:
            classroom = db.session.query(Classroom).filter_by(id=id).first()
            if not classroom:
                return error_response(
                    error_code=ClassroomErrorResponse.NOT_FOUND.name,
                    status_code=ClassroomErrorResponse.NOT_FOUND.value
                    .get("status_code"),
                    message=ClassroomErrorResponse.NOT_FOUND.value
                    .get("message")
                )

            db.session.delete(classroom)
            db.session.commit()
            return success_response(
                message_key=ClassroomSuccessResponse.DELETED.value
                .get("message"),
                status_code=ClassroomSuccessResponse.DELETED.value
                .get("status_code")
            )
        except Exception as e:
            logging.error(f"Unexpected error: {e}")
            return error_response(
                error_code=ClassroomErrorResponse.UNEXPECTED_ERROR.name,
                status_code=ClassroomErrorResponse.UNEXPECTED_ERROR.value
                .get("status_code"),
                message=ClassroomErrorResponse.UNEXPECTED_ERROR.value
                .get("message")
            )


class ClassroomListResource(Resource):
    @swag_from('../docs/classrooms/get_all.yml')
    def get(self):
        try:
            classrooms = db.session.query(Classroom).all()
            result = [{
                "id": c.id,
                "number": c.number,
                "pavilion_id": c.pavilion_id
            } for c in classrooms]
            return success_response(
                message_key=ClassroomSuccessResponse.LIST_RETRIEVED.value
                .get("message"),
                status_code=ClassroomSuccessResponse.LIST_RETRIEVED.value
                .get("status_code"),
                data=result
            )
        except Exception as e:
            logging.error(f"Unexpected error: {e}")
            return error_response(
                error_code=ClassroomErrorResponse.UNEXPECTED_ERROR.name,
                status_code=ClassroomErrorResponse.UNEXPECTED_ERROR.value
                .get("status_code"),
                message=ClassroomErrorResponse.UNEXPECTED_ERROR.value
                .get("message")
            )

    @swag_from('../docs/classrooms/post.yml')
    def post(self):
        try:
            data = request.json
            number = data.get("number")
            pavilion_id = data.get("pavilion_id")

            if number is None or pavilion_id is None:
                return error_response(
                    error_code=ClassroomErrorResponse.MISSING_FIELDS.name,
                    status_code=ClassroomErrorResponse.MISSING_FIELDS.value
                    .get("status_code"),
                    message=ClassroomErrorResponse.MISSING_FIELDS.value
                    .get("message")
                )

            new_classroom = Classroom(
                id=uuid.uuid4(),
                number=number,
                pavilion_id=pavilion_id
            )
            db.session.add(new_classroom)
            db.session.commit()

            response = {
                "id": new_classroom.id,
                "number": new_classroom.number,
                "pavilion_id": new_classroom.pavilion_id
            }
            return success_response(
                message_key=ClassroomSuccessResponse.CREATED.value
                .get("message"),
                status_code=ClassroomSuccessResponse.CREATED.value
                .get("status_code"),
                data=response
            )
        except Exception as e:
            logging.error(f"Unexpected error: {e}")
            return error_response(
                error_code=ClassroomErrorResponse.UNEXPECTED_ERROR.name,
                status_code=ClassroomErrorResponse.UNEXPECTED_ERROR.value
                .get("status_code"),
                message=ClassroomErrorResponse.UNEXPECTED_ERROR.value
                .get("message")
            )
"""