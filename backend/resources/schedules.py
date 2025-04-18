import uuid
import logging
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource, request
from flasgger.utils import swag_from
from models.pavilion import Pavilion
from utils.responses import success_response, error_response
from database.db import db
from models.schedule import Schedule
from responses.schedules_response import ScheduleErrorResponse, ScheduleSuccessResponse

logging.basicConfig(level=logging.INFO)


class ScheduleResource(Resource):
    @jwt_required()
    @swag_from('../docs/schedules/get.yml')
    def get(self, id):
        try:
            user_id = get_jwt_identity()
            logging.info(f"user_id: {user_id}, schedule_id: {id}")

            schedule = db.session.query(Schedule).filter_by(id=id, user_id=user_id).first()

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
                    "pavilion": schedule.pavilion,
                    "block": schedule.block,
                    "classroom": schedule.classroom,
                    "day": schedule.day,
                    "subject": schedule.subject,
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

    @jwt_required()
    @swag_from('../docs/schedules/put.yml')
    def put(self, id):
        try:
            user_id = get_jwt_identity()
            data = request.get_json()
            schedule = db.session.query(Schedule).filter_by(id=id, user_id=user_id).first()
            if not schedule:
                return error_response(
                    error_code=ScheduleErrorResponse.NOT_FOUND.name,
                    status_code=ScheduleErrorResponse.NOT_FOUND.value.get("status_code"),
                    message=ScheduleErrorResponse.NOT_FOUND.value.get("message")
                )

            for field in ['pavilion', 'block', 'classroom', 'day', 'subject']:
                if field in data:
                    setattr(schedule, field, data[field])

            db.session.commit()

            return success_response(
                message_key=ScheduleSuccessResponse.UPDATED.value.get("message"),
                status_code=ScheduleSuccessResponse.UPDATED.value.get("status_code"),
                data={
                    "id": str(schedule.id),
                    "pavilion": schedule.pavilion,
                    "block": schedule.block,
                    "classroom": schedule.classroom,
                    "day": schedule.day,
                    "subject": schedule.subject,
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

    @jwt_required()
    @swag_from('../docs/schedules/delete.yml')
    def delete(self, id):
        try:
            user_id = get_jwt_identity()
            schedule = db.session.query(Schedule).filter_by(id=id, user_id=user_id).first()
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
    @jwt_required()
    @swag_from('../docs/schedules/get_all.yml')
    def get(self):
        try:
            user_id = get_jwt_identity()
            schedules = db.session.query(Schedule).filter_by(user_id=user_id).all()
            result = [{
                "id": str(s.id),
                "pavilion": s.pavilion,
                "block": s.block,
                "classroom": s.classroom,
                "day": s.day,
                "subject": s.subject,
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

    @jwt_required()
    @swag_from('../docs/schedules/post.yml')
    def post(self):
        try:
            user_id = get_jwt_identity()
            data = request.get_json()

            required_fields = ['schedules']
            if not all(field in data for field in required_fields):
                return error_response(
                    error_code=ScheduleErrorResponse.MISSING_FIELDS.name,
                    status_code=ScheduleErrorResponse.MISSING_FIELDS.value.get("status_code"),
                    message=ScheduleErrorResponse.MISSING_FIELDS.value.get("message")
                )

            schedules_data = data['schedules']

            for schedule_data in schedules_data:
                required_fields = ['pavilion', 'block', 'classroom', 'day', 'subject']
                if not all(field in schedule_data for field in required_fields):
                    return error_response(
                        error_code=ScheduleErrorResponse.MISSING_FIELDS.name,
                        status_code=ScheduleErrorResponse.MISSING_FIELDS.value.get("status_code"),
                        message=ScheduleErrorResponse.MISSING_FIELDS.value.get("message")
                    )

             
                pavilion_name = schedule_data['pavilion']
                name_pavilion = db.session.query(Pavilion).filter_by(name=pavilion_name).first()

                if not name_pavilion:
                    return error_response(
                        error_code=ScheduleErrorResponse.INVALID_PAVILION.name,
                        status_code=ScheduleErrorResponse.INVALID_PAVILION.value.get("status_code"),
                        message=f"Pavilion '{pavilion_name}' not found."
                    )

                
                existing_schedule = db.session.query(Schedule).filter_by(
                    pavilion=schedule_data['pavilion'],
                    block=schedule_data['block'],
                    classroom=schedule_data['classroom'],
                    day=schedule_data['day'].lower(),
                    subject=schedule_data['subject'],
                    user_id=user_id
                ).first()

                if existing_schedule:
                    return error_response(
                        error_code=ScheduleErrorResponse.SCHEDULE_ALREADY_EXISTS.name,
                        status_code=ScheduleErrorResponse.SCHEDULE_ALREADY_EXISTS.value.get("status_code"),
                        message=f"Schedule already exists for the given parameters: {schedule_data['pavilion']}, {schedule_data['block']}, {schedule_data['classroom']}, {schedule_data['day']}, {schedule_data['subject']}"
                    )

            
            new_schedules = []
            for schedule_data in schedules_data:
                new_schedule = Schedule(
                    id=uuid.uuid4(),
                    pavilion=schedule_data['pavilion'],
                    block=schedule_data['block'],
                    classroom=schedule_data['classroom'],
                    day=schedule_data['day'],
                    subject=schedule_data['subject'],
                    user_id=user_id
                )
                db.session.add(new_schedule)
                new_schedules.append({
                    "id": str(new_schedule.id),
                    "pavilion": new_schedule.pavilion,
                    "block": new_schedule.block,
                    "classroom": new_schedule.classroom,
                    "day": new_schedule.day,
                    "subject": new_schedule.subject,
                    "user_id": str(new_schedule.user_id) if new_schedule.user_id else None
                })

            db.session.commit()

            return success_response(
                message_key=ScheduleSuccessResponse.CREATED.value.get("message"),
                status_code=ScheduleSuccessResponse.CREATED.value.get("status_code"),
                data={
                    "success": True,
                    "message": "Schedules created successfully.",
                    "data": new_schedules
                }
            )

        except Exception as e:
            logging.error(f"Error creating schedule: {e}")
            return error_response(
                error_code=ScheduleErrorResponse.UNEXPECTED_ERROR.name,
                status_code=ScheduleErrorResponse.UNEXPECTED_ERROR.value.get("status_code"),
                message=ScheduleErrorResponse.UNEXPECTED_ERROR.value.get("message")
            )


