import uuid
import logging
from flask_restful import Resource, request
from flasgger.utils import swag_from
from utils.responses import success_response, error_response
from database.db import db
from models.pavilion import Pavilion
from responses.pavilion_response import (
    PavilionErrorResponse,
    PavilionSuccessResponse
)

logging.basicConfig(level=logging.INFO)


class PavilionResource(Resource):
    @swag_from('../docs/pavilions/get.yml')
    def get(self, id):
        try:
            pavilion = db.session.query(Pavilion).filter_by(id=id).first()
            if not pavilion:
                return error_response(
                    error_code=PavilionErrorResponse.NOT_FOUND.name,
                    status_code=PavilionErrorResponse.NOT_FOUND.value.get("status_code"),
                    message=PavilionErrorResponse.NOT_FOUND.value.get("message")
                )

            return success_response(
                message_key=PavilionSuccessResponse.RETRIEVED.value.get("message"),
                status_code=PavilionSuccessResponse.RETRIEVED.value.get("status_code"),
                data={
                    "id": str(pavilion.id),
                    "name": pavilion.name,
                    "x": pavilion.x,
                    "y": pavilion.y
                }
            )
        except Exception as e:
            logging.error(f"Unexpected error during get pavilion: {e}")
            return error_response(
                error_code=PavilionErrorResponse.UNEXPECTED_ERROR.name,
                status_code=PavilionErrorResponse.UNEXPECTED_ERROR.value.get("status_code"),
                message=PavilionErrorResponse.UNEXPECTED_ERROR.value.get("message")
            )
        
    
    @swag_from('../docs/pavilions/put.yml')
    def put(self, id):
        try:
            data = request.get_json()
            name = data.get("name")
            x = data.get("x")
            y = data.get("y")

            pavilion = db.session.query(Pavilion).filter_by(id=id).first()
            if not pavilion:
                return error_response(
                    error_code=PavilionErrorResponse.NOT_FOUND.name,
                    status_code=PavilionErrorResponse.NOT_FOUND.value.get("status_code"),
                    message=PavilionErrorResponse.NOT_FOUND.value.get("message")
                )

            if name: pavilion.name = name
            if x is not None: pavilion.x = x
            if y is not None: pavilion.y = y

            db.session.commit()

            return success_response(
                message_key=PavilionSuccessResponse.UPDATED.value.get("message"),
                status_code=PavilionSuccessResponse.UPDATED.value.get("status_code"),
                data={
                    "id": str(pavilion.id),
                    "name": pavilion.name,
                    "x": pavilion.x,
                    "y": pavilion.y
                }
            )

        except Exception as e:
            logging.error(f"Unexpected error during put pavilion: {e}")
            return error_response(
                error_code=PavilionErrorResponse.UNEXPECTED_ERROR.name,
                status_code=PavilionErrorResponse.UNEXPECTED_ERROR.value.get("status_code"),
                message=PavilionErrorResponse.UNEXPECTED_ERROR.value.get("message")
            )

    @swag_from('../docs/pavilions/delete.yml')
    def delete(self, id):
        try:
            pavilion = db.session.query(Pavilion).filter_by(id=id).first()
            if not pavilion:
                return error_response(
                    error_code=PavilionErrorResponse.NOT_FOUND.name,
                    status_code=PavilionErrorResponse.NOT_FOUND.value.get("status_code"),
                    message=PavilionErrorResponse.NOT_FOUND.value.get("message")
                )

            db.session.delete(pavilion)
            db.session.commit()

            return success_response(
                message_key=PavilionSuccessResponse.DELETED.value.get("message"),
                status_code=PavilionSuccessResponse.DELETED.value.get("status_code")
            )

        except Exception as e:
            logging.error(f"Unexpected error during delete pavilion: {e}")
            return error_response(
                error_code=PavilionErrorResponse.UNEXPECTED_ERROR.name,
                status_code=PavilionErrorResponse.UNEXPECTED_ERROR.value.get("status_code"),
                message=PavilionErrorResponse.UNEXPECTED_ERROR.value.get("message")
            )


class PavilionByNameResource(Resource):
    @swag_from('../docs/pavilions/get_name.yml')
    def get(self, name):
        try:
            pavilion = db.session.query(Pavilion).filter_by(name=name).first()
            if not pavilion:
                return error_response(
                    error_code=PavilionErrorResponse.NOT_FOUND.name,
                    status_code=PavilionErrorResponse.NOT_FOUND.value.get("status_code"),
                    message=PavilionErrorResponse.NOT_FOUND.value.get("message")
                )

            return success_response(
                message_key=PavilionSuccessResponse.RETRIEVED.value.get("message"),
                status_code=PavilionSuccessResponse.RETRIEVED.value.get("status_code"),
                data={
                    "id": str(pavilion.id),
                    "name": pavilion.name,
                    "x": pavilion.x,
                    "y": pavilion.y
                }
            )
        except Exception as e:
            logging.error(f"Unexpected error during get pavilion: {e}")
            return error_response(
                error_code=PavilionErrorResponse.UNEXPECTED_ERROR.name,
                status_code=PavilionErrorResponse.UNEXPECTED_ERROR.value.get("status_code"),
                message=PavilionErrorResponse.UNEXPECTED_ERROR.value.get("message")
            )


class PavilionListResource(Resource):
    @swag_from('../docs/pavilions/get_all.yml')
    def get(self):
        try:
            pavilions = db.session.query(Pavilion).all()
            result = [{
                "id": str(p.id),
                "name": p.name,
                "x": p.x,
                "y": p.y
            } for p in pavilions]

            return success_response(
                message_key=PavilionSuccessResponse.LIST_RETRIEVED.value.get("message"),
                status_code=PavilionSuccessResponse.LIST_RETRIEVED.value.get("status_code"),
                data=result
            )
        except Exception as e:
            logging.error(f"Unexpected error during get pavilions: {e}")
            return error_response(
                error_code=PavilionErrorResponse.UNEXPECTED_ERROR.name,
                status_code=PavilionErrorResponse.UNEXPECTED_ERROR.value.get("status_code"),
                message=PavilionErrorResponse.UNEXPECTED_ERROR.value.get("message")
            )

    @swag_from('../docs/pavilions/post.yml')
    def post(self):
        try:
            data = request.get_json()
            name = data.get("name", "").upper()
            x = data.get("x")
            y = data.get("y")

            if not name or x is None or y is None:
                return error_response(
                    error_code=PavilionErrorResponse.MISSING_FIELDS.name,
                    status_code=PavilionErrorResponse.MISSING_FIELDS.value.get("status_code"),
                    message=PavilionErrorResponse.MISSING_FIELDS.value.get("message")
                )

            new_pavilion = Pavilion(id=uuid.uuid4(), name=name, x=x, y=y)
            db.session.add(new_pavilion)
            db.session.commit()

            return success_response(
                message_key=PavilionSuccessResponse.CREATED.value.get("message"),
                status_code=PavilionSuccessResponse.CREATED.value.get("status_code"),
                data={
                    "id": str(new_pavilion.id),
                    "name": new_pavilion.name,
                    "x": new_pavilion.x,
                    "y": new_pavilion.y
                }
            )

        except Exception as e:
            logging.error(f"Unexpected error during post pavilion: {e}")
            return error_response(
                error_code=PavilionErrorResponse.UNEXPECTED_ERROR.name,
                status_code=PavilionErrorResponse.UNEXPECTED_ERROR.value.get("status_code"),
                message=PavilionErrorResponse.UNEXPECTED_ERROR.value.get("message")
            )
