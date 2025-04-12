import logging
import uuid
from flask_restful import Resource, request
from flasgger.utils import swag_from
from database.db import db
from models.schedule import Schedule
from utils.responses import success_response, error_response
from responses.schedules_response import (
    ScheduleErrorResponse,
    ScheduleSuccessResponse
)

logging.basicConfig(level=logging.INFO)


class ScheduleResource(Resource):
    @swag_from('../docs/schedules/get.yml')
    def get(self, schedule_id):
        try:
            schedule = db.session.query(Schedule) \
                .filter_by(id=schedule_id) \
                .first()
            if not schedule:
                return error_response(
                    error_code=ScheduleErrorResponse.NOT_FOUND.name,
                    status_code=ScheduleErrorResponse.NOT_FOUND.value
                    .get("status_code"),
                    message=ScheduleErrorResponse.NOT_FOUND.value
                    .get("message")
                )

            result = {
                "id": schedule.id,
                "user_id": schedule.user_id,
                "subject_id": schedule.subject_id,
                "classroom_id": schedule.classroom_id,
                "date": schedule.date.isoformat(),
                "start": str(schedule.start),
                "end": str(schedule.end),
            }
            return success_response(
                message_key=ScheduleSuccessResponse.RETRIEVED.value
                .get("message"),
                status_code=ScheduleSuccessResponse.RETRIEVED.value
                .get("status_code"),
                data=result
            )

        except Exception as e:
            logging.error(f"Unexpected error during get schedule: {e}")
            return error_response(
                error_code=ScheduleErrorResponse.UNEXPECTED_ERROR.name,
                status_code=ScheduleErrorResponse.UNEXPECTED_ERROR.value
                .get("status_code"),
                message=ScheduleErrorResponse.UNEXPECTED_ERROR.value
                .get("message")
            )

    @swag_from('../docs/schedules/put.yml')
    def put(self, schedule_id):
        try:
            schedule = db.session \
                .query(Schedule) \
                .filter_by(id=schedule_id) \
                .first()
            if not schedule:
                return error_response(
                    error_code=ScheduleErrorResponse.NOT_FOUND.name,
                    status_code=ScheduleErrorResponse.NOT_FOUND.value
                    .get("status_code"),
                    message=ScheduleErrorResponse.NOT_FOUND.value
                    .get("message")
                )

            data = request.json
            schedule.user_id = data.get("user_id", schedule.user_id)
            schedule.subject_id = data.get("subject_id", schedule.subject_id)
            schedule.classroom_id = data.get(
                "classroom_id",
                schedule.classroom_id
            )
            schedule.date = data.get("date", schedule.date)
            schedule.start = data.get("start", schedule.start)
            schedule.end = data.get("end", schedule.end)

            db.session.commit()

            result = {
                "id": schedule.id,
                "user_id": schedule.user_id,
                "subject_id": schedule.subject_id,
                "classroom_id": schedule.classroom_id,
                "date": schedule.date.isoformat(),
                "start": str(schedule.start),
                "end": str(schedule.end),
            }

            return success_response(
                message_key=ScheduleSuccessResponse.UPDATED.value
                .get("message"),
                status_code=ScheduleSuccessResponse.UPDATED.value
                .get("status_code"),
                data=result
            )

        except Exception as e:
            logging.error(f"Unexpected error during put schedule: {e}")
            return error_response(
                error_code=ScheduleErrorResponse.UNEXPECTED_ERROR.name,
                status_code=ScheduleErrorResponse.UNEXPECTED_ERROR.value
                .get("status_code"),
                message=ScheduleErrorResponse.UNEXPECTED_ERROR.value
                .get("message")
            )

    @swag_from('../docs/schedules/delete.yml')
    def delete(self, schedule_id):
        try:
            schedule = db.session \
                .query(Schedule) \
                .filter_by(id=schedule_id) \
                .first()
            if not schedule:
                return error_response(
                    error_code=ScheduleErrorResponse.NOT_FOUND.name,
                    status_code=ScheduleErrorResponse.NOT_FOUND.value
                    .get("status_code"),
                    message=ScheduleErrorResponse.NOT_FOUND.value
                    .get("message")
                )

            db.session.delete(schedule)
            db.session.commit()

            return success_response(
                message_key=ScheduleSuccessResponse.DELETED.value
                .get("message"),
                status_code=ScheduleSuccessResponse.DELETED.value
                .get("status_code")
            )

        except Exception as e:
            logging.error(f"Unexpected error during delete schedule: {e}")
            return error_response(
                error_code=ScheduleErrorResponse.UNEXPECTED_ERROR.name,
                status_code=ScheduleErrorResponse.UNEXPECTED_ERROR.value
                .get("status_code"),
                message=ScheduleErrorResponse.UNEXPECTED_ERROR.value
                .get("message")
            )


class ScheduleListResource(Resource):
    @swag_from('../docs/schedules/get_all.yml')
    def get(self):
        try:
            schedules = db.session.query(Schedule).all()
            result = [{
                "id": s.id,
                "user_id": s.user_id,
                "subject_id": s.subject_id,
                "classroom_id": s.classroom_id,
                "date": s.date.isoformat(),
                "start": str(s.start),
                "end": str(s.end),
            } for s in schedules]

            return success_response(
                message_key=ScheduleSuccessResponse.LIST_RETRIEVED.value
                .get("message"),
                status_code=ScheduleSuccessResponse.LIST_RETRIEVED.value
                .get("status_code"),
                data=result
            )

        except Exception as e:
            logging.error(f"Unexpected error during get schedules: {e}")
            return error_response(
                error_code=ScheduleErrorResponse.UNEXPECTED_ERROR.name,
                status_code=ScheduleErrorResponse.UNEXPECTED_ERROR.value
                .get("status_code"),
                message=ScheduleErrorResponse.UNEXPECTED_ERROR.value
                .get("message")
            )

    @swag_from('../docs/schedules/post.yml')
    def post(self):
        try:
            data = request.json
            required_fields = [
                "user_id",
                "subject_id",
                "classroom_id",
                "date",
                "start",
                "end"
            ]
            if not all(field in data for field in required_fields):
                return error_response(
                    error_code=ScheduleErrorResponse.MISSING_FIELDS.name,
                    status_code=ScheduleErrorResponse.MISSING_FIELDS.value
                    .get("status_code"),
                    message=ScheduleErrorResponse.MISSING_FIELDS.value
                    .get("message")
                )

            new_schedule = Schedule(
                id=uuid.uuid4(),
                user_id=data["user_id"],
                subject_id=data["subject_id"],
                classroom_id=data["classroom_id"],
                date=data["date"],
                start=data["start"],
                end=data["end"]
            )

            db.session.add(new_schedule)
            db.session.commit()

            result = {
                "id": new_schedule.id,
                "user_id": new_schedule.user_id,
                "subject_id": new_schedule.subject_id,
                "classroom_id": new_schedule.classroom_id,
                "date": new_schedule.date.isoformat(),
                "start": str(new_schedule.start),
                "end": str(new_schedule.end),
            }

            return success_response(
                message_key=ScheduleSuccessResponse.CREATED.value
                .get("message"),
                status_code=ScheduleSuccessResponse.CREATED.value
                .get("status_code"),
                data=result
            )

        except Exception as e:
            logging.error(f"Unexpected error during post schedules: {e}")
            return error_response(
                error_code=ScheduleErrorResponse.UNEXPECTED_ERROR.name,
                status_code=ScheduleErrorResponse.UNEXPECTED_ERROR.value
                .get("status_code"),
                message=ScheduleErrorResponse.UNEXPECTED_ERROR.value
                .get("message")
            )
