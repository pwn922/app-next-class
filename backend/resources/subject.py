import uuid
import logging
from flask_restful import Resource, request
from flasgger.utils import swag_from
from database.db import db
from models.subject import Subject
from utils.responses import success_response, error_response
from responses.subject_response import (
    SubjectSuccessResponse,
    SubjectErrorResponse
)

logging.basicConfig(level=logging.INFO)


class SubjectResource(Resource):
    @swag_from('../docs/subjects/get.yml')
    def get(self, id):
        try:
            subject = db.session.query(Subject).filter_by(id=id).first()
            if not subject:
                return error_response(
                    error_code=SubjectErrorResponse.NOT_FOUND.name,
                    status_code=SubjectErrorResponse.NOT_FOUND.value
                    .get("status_code"),
                    message=SubjectErrorResponse.NOT_FOUND.value
                    .get("message")
                )

            return success_response(
                message_key=SubjectSuccessResponse.RETRIEVED.value
                .get("message"),
                status_code=SubjectSuccessResponse.RETRIEVED.value
                .get("status_code"),
                data={
                    "id": str(subject.id),
                    "name": subject.name,
                    "code": subject.code
                }
            )
        except Exception as e:
            logging.error(f"Unexpected error during get subject: {e}")
            return error_response(
                error_code=SubjectErrorResponse.UNEXPECTED_ERROR.name,
                status_code=SubjectErrorResponse.UNEXPECTED_ERROR.value
                .get("status_code"),
                message=SubjectErrorResponse.UNEXPECTED_ERROR.value
                .get("message")
            )

    @swag_from('../docs/subjects/put.yml')
    def put(self, id):
        try:
            subject = db.session.query(Subject).filter_by(id=id).first()
            if not subject:
                return error_response(
                    error_code=SubjectErrorResponse.NOT_FOUND.name,
                    status_code=SubjectErrorResponse.NOT_FOUND.value
                    .get("status_code"),
                    message=SubjectErrorResponse.NOT_FOUND.value
                    .get("message")
                )

            data = request.json
            subject.name = data.get("name", subject.name)
            subject.code = data.get("code", subject.code)
            db.session.commit()

            return success_response(
                message_key=SubjectSuccessResponse.UPDATED.value
                .get("message"),
                status_code=SubjectSuccessResponse.UPDATED.value
                .get("status_code"),
                data={
                    "id": str(subject.id),
                    "name": subject.name,
                    "code": subject.code
                }
            )
        except Exception as e:
            logging.error(f"Unexpected error during put subject: {e}")
            return error_response(
                error_code=SubjectErrorResponse.UNEXPECTED_ERROR.name,
                status_code=SubjectErrorResponse.UNEXPECTED_ERROR.value
                .get("status_code"),
                message=SubjectErrorResponse.UNEXPECTED_ERROR.value
                .get("message")
            )

    @swag_from('../docs/subjects/delete.yml')
    def delete(self, id):
        try:
            subject = db.session.query(Subject).filter_by(id=id).first()
            if not subject:
                return error_response(
                    error_code=SubjectErrorResponse.NOT_FOUND.name,
                    status_code=SubjectErrorResponse.NOT_FOUND.value
                    .get("status_code"),
                    message=SubjectErrorResponse.NOT_FOUND.value
                    .get("message")
                )

            db.session.delete(subject)
            db.session.commit()

            return success_response(
                message_key=SubjectSuccessResponse.DELETED.value
                .get("message"),
                status_code=SubjectSuccessResponse.DELETED.value
                .get("status_code")
            )
        except Exception as e:
            logging.error(f"Unexpected error during delete subject: {e}")
            return error_response(
                error_code=SubjectErrorResponse.UNEXPECTED_ERROR.name,
                status_code=SubjectErrorResponse.UNEXPECTED_ERROR.value
                .get("status_code"),
                message=SubjectErrorResponse.UNEXPECTED_ERROR.value
                .get("message")
            )


class SubjectListResource(Resource):
    @swag_from('../docs/subjects/get_all.yml')
    def get(self):
        try:
            subjects = db.session.query(Subject).all()
            result = [
                {"id": str(s.id), "name": s.name, "code": s.code}
                for s in subjects
            ]
            return success_response(
                message_key=SubjectSuccessResponse.LIST_RETRIEVED.value
                .get("message"),
                status_code=SubjectSuccessResponse.LIST_RETRIEVED.value
                .get("status_code"),
                data=result
            )
        except Exception as e:
            logging.error(f"Unexpected error during get subjects: {e}")
            logging.error(f"Unexpected error: {e}")
            return error_response(
                error_code=SubjectErrorResponse.UNEXPECTED_ERROR.name,
                status_code=SubjectErrorResponse.UNEXPECTED_ERROR.value
                .get("status_code"),
                message=SubjectErrorResponse.UNEXPECTED_ERROR.value
                .get("message")
            )

    @swag_from('../docs/subjects/post.yml')
    def post(self):
        try:
            data = request.json
            name = data.get("name")
            code = data.get("code")

            if not name or not code:
                return error_response(
                    error_code=SubjectErrorResponse.MISSING_FIELDS.name,
                    status_code=SubjectErrorResponse.MISSING_FIELDS.value
                    .get("status_code"),
                    message=SubjectErrorResponse.MISSING_FIELDS.value
                    .get("message")
                )

            new_subject = Subject(id=uuid.uuid4(), name=name, code=code)
            db.session.add(new_subject)
            db.session.commit()

            response = {
                "id": str(new_subject.id),
                "name": new_subject.name,
                "code": new_subject.code
            }

            return success_response(
                message_key=SubjectSuccessResponse.CREATED.value
                .get("message"),
                status_code=SubjectSuccessResponse.CREATED.value
                .get("status_code"),
                data=response
            )
        except Exception as e:
            logging.error(f"Unexpected error during post subjects: {e}")
            return error_response(
                error_code=SubjectErrorResponse.UNEXPECTED_ERROR.name,
                status_code=SubjectErrorResponse.UNEXPECTED_ERROR.value
                .get("status_code"),
                message=SubjectErrorResponse.UNEXPECTED_ERROR.value
                .get("message")
            )
