import uuid
import logging
from flask_restful import Resource, request
from flasgger.utils import swag_from
from utils.responses import success_response, error_response
from database.db import db
from models.schedule import Schedule
from responses.schedules_response import ScheduleErrorResponse, ScheduleSuccessResponse

logging.basicConfig(level=logging.INFO)


class ScheduleResource(Resource):
    @swag_from('../docs/schedules/get.yml')
    def get(self, id):
        try:
            schedule = db.session.query(Schedule).filter_by(id=id).first()
            if not schedule:
                return error_response(
                    error_code=ScheduleErrorResponse.NOT_FOUND.name,
                    status_code=ScheduleErrorResponse.NOT_FOUND.value.get("status_code"),
                    message=ScheduleErrorResponse.NOT_FOUND.value.get("message")
                )

            return success_response(
                message_key=ScheduleSuccessResponse.RETRIEVED.value.get("message"),
                status_code=ScheduleSuccessResponse.RETRIEVED.value.get("status_code"),
                data={
                    "id": str(schedule.id),
                    "departamento": schedule.departamento,
                    "bloque": schedule.bloque,
                    "sala": schedule.sala,
                    "dia": schedule.dia,
                    "asignatura": schedule.asignatura,
                    "user_id": str(schedule.user_id) if schedule.user_id else None
                }
            )
        except Exception as e:
            logging.error(f"Error retrieving schedule: {e}")
            return error_response(
                error_code=ScheduleErrorResponse.UNEXPECTED_ERROR.name,
                status_code=ScheduleErrorResponse.UNEXPECTED_ERROR.value.get("status_code"),
                message=ScheduleErrorResponse.UNEXPECTED_ERROR.value.get("message")
            )

    @swag_from('../docs/schedules/put.yml')
    def put(self, id):
        try:
            data = request.get_json()
            schedule = db.session.query(Schedule).filter_by(id=id).first()
            if not schedule:
                return error_response(
                    error_code=ScheduleErrorResponse.NOT_FOUND.name,
                    status_code=ScheduleErrorResponse.NOT_FOUND.value.get("status_code"),
                    message=ScheduleErrorResponse.NOT_FOUND.value.get("message")
                )

            for field in ['departamento', 'bloque', 'sala', 'dia', 'asignatura', 'user_id']:
                if field in data:
                    setattr(schedule, field, data[field])

            db.session.commit()

            return success_response(
                message_key=ScheduleSuccessResponse.UPDATED.value.get("message"),
                status_code=ScheduleSuccessResponse.UPDATED.value.get("status_code"),
                data={
                    "id": str(schedule.id),
                    "departamento": schedule.departamento,
                    "bloque": schedule.bloque,
                    "sala": schedule.sala,
                    "dia": schedule.dia,
                    "asignatura": schedule.asignatura,
                    "user_id": str(schedule.user_id) if schedule.user_id else None
                }
            )

        except Exception as e:
            logging.error(f"Error updating schedule: {e}")
            return error_response(
                error_code=ScheduleErrorResponse.UNEXPECTED_ERROR.name,
                status_code=ScheduleErrorResponse.UNEXPECTED_ERROR.value.get("status_code"),
                message=ScheduleErrorResponse.UNEXPECTED_ERROR.value.get("message")
            )

    @swag_from('../docs/schedules/delete.yml')
    def delete(self, id):
        try:
            schedule = db.session.query(Schedule).filter_by(id=id).first()
            if not schedule:
                return error_response(
                    error_code=ScheduleErrorResponse.NOT_FOUND.name,
                    status_code=ScheduleErrorResponse.NOT_FOUND.value.get("status_code"),
                    message=ScheduleErrorResponse.NOT_FOUND.value.get("message")
                )

            db.session.delete(schedule)
            db.session.commit()

            return success_response(
                message_key=ScheduleSuccessResponse.DELETED.value.get("message"),
                status_code=ScheduleSuccessResponse.DELETED.value.get("status_code")
            )

        except Exception as e:
            logging.error(f"Error deleting schedule: {e}")
            return error_response(
                error_code=ScheduleErrorResponse.UNEXPECTED_ERROR.name,
                status_code=ScheduleErrorResponse.UNEXPECTED_ERROR.value.get("status_code"),
                message=ScheduleErrorResponse.UNEXPECTED_ERROR.value.get("message")
            )


class ScheduleListResource(Resource):
    @swag_from('../docs/schedules/get_all.yml')
    def get(self):
        try:
            schedules = db.session.query(Schedule).all()
            result = [{
                "id": str(s.id),
                "departamento": s.departamento,
                "bloque": s.bloque,
                "sala": s.sala,
                "dia": s.dia,
                "asignatura": s.asignatura,
                "user_id": str(s.user_id) if s.user_id else None
            } for s in schedules]

            return success_response(
                message_key=ScheduleSuccessResponse.LIST_RETRIEVED.value.get("message"),
                status_code=ScheduleSuccessResponse.LIST_RETRIEVED.value.get("status_code"),
                data=result
            )
        except Exception as e:
            logging.error(f"Error listing schedules: {e}")
            return error_response(
                error_code=ScheduleErrorResponse.UNEXPECTED_ERROR.name,
                status_code=ScheduleErrorResponse.UNEXPECTED_ERROR.value.get("status_code"),
                message=ScheduleErrorResponse.UNEXPECTED_ERROR.value.get("message")
            )

    @swag_from('../docs/schedules/post.yml')
    def post(self):
        try:
            data = request.get_json()
            required_fields = ['departamento', 'bloque', 'sala', 'dia', 'asignatura']
            if not all(field in data for field in required_fields):
                return error_response(
                    error_code=ScheduleErrorResponse.MISSING_FIELDS.name,
                    status_code=ScheduleErrorResponse.MISSING_FIELDS.value.get("status_code"),
                    message=ScheduleErrorResponse.MISSING_FIELDS.value.get("message")
                )

            new_schedule = Schedule(
                id=uuid.uuid4(),
                departamento=data['departamento'],
                bloque=data['bloque'],
                sala=data['sala'],
                dia=data['dia'],
                asignatura=data['asignatura'],
                user_id=data.get('user_id')
            )
            db.session.add(new_schedule)
            db.session.commit()

            return success_response(
                message_key=ScheduleSuccessResponse.CREATED.value.get("message"),
                status_code=ScheduleSuccessResponse.CREATED.value.get("status_code"),
                data={
                    "id": str(new_schedule.id),
                    "departamento": new_schedule.departamento,
                    "bloque": new_schedule.bloque,
                    "sala": new_schedule.sala,
                    "dia": new_schedule.dia,
                    "asignatura": new_schedule.asignatura,
                    "user_id": str(new_schedule.user_id) if new_schedule.user_id else None
                }
            )

        except Exception as e:
            logging.error(f"Error creating schedule: {e}")
            return error_response(
                error_code=ScheduleErrorResponse.UNEXPECTED_ERROR.name,
                status_code=ScheduleErrorResponse.UNEXPECTED_ERROR.value.get("status_code"),
                message=ScheduleErrorResponse.UNEXPECTED_ERROR.value.get("message")
            )
