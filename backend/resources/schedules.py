import uuid
from flask_restful import Resource, request
from flasgger.utils import swag_from
from flask import jsonify, make_response
from database.db import db
from models.schedule import Schedule

class ScheduleResource(Resource):
    @swag_from('../docs/schedules/get.yml')
    def get(self, schedule_id):
        try:
            schedule = db.session.query(Schedule).filter_by(id=schedule_id).first()
            if not schedule:
                return make_response(jsonify({"error": "Schedule not found"}), 404)

            result = {
                "id": schedule.id,
                "user_id": schedule.user_id,
                "subject_id": schedule.subject_id,
                "classroom_id": schedule.classroom_id,
                "date": schedule.date.isoformat(),
                "start": str(schedule.start),
                "end": str(schedule.end),
            }
            return make_response(jsonify(result), 200)

        except Exception as e:
            return make_response(jsonify({"error": str(e)}), 500)

    @swag_from('../docs/schedules/put.yml')
    def put(self, schedule_id):
        try:
            schedule = db.session.query(Schedule).filter_by(id=schedule_id).first()
            if not schedule:
                return make_response(jsonify({"error": "Schedule not found"}), 404)

            data = request.json

            schedule.user_id = data.get("user_id", schedule.user_id)
            schedule.subject_id = data.get("subject_id", schedule.subject_id)
            schedule.classroom_id = data.get("classroom_id", schedule.classroom_id)
            schedule.date = data.get("date", schedule.date)
            schedule.start = data.get("start", schedule.start)
            schedule.end = data.get("end", schedule.end)

            db.session.commit()

            return make_response(jsonify({
                "id": schedule.id,
                "user_id": schedule.user_id,
                "subject_id": schedule.subject_id,
                "classroom_id": schedule.classroom_id,
                "date": schedule.date.isoformat(),
                "start": str(schedule.start),
                "end": str(schedule.end),
            }), 200)

        except Exception as e:
            return make_response(jsonify({"error": str(e)}), 500)

    @swag_from('../docs/schedules/delete.yml')
    def delete(self, schedule_id):
        try:
            schedule = db.session.query(Schedule).filter_by(id=schedule_id).first()
            if not schedule:
                return make_response(jsonify({"error": "Schedule not found"}), 404)

            db.session.delete(schedule)
            db.session.commit()

            return make_response('', 204)

        except Exception as e:
            return make_response(jsonify({"error": str(e)}), 500)


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

            return make_response(jsonify(result), 200)

        except Exception as e:
            return make_response(jsonify({"error": str(e)}), 500)

    @swag_from('../docs/schedules/post.yml')
    def post(self):
        try:
            data = request.json

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

            return make_response(jsonify({
                "id": new_schedule.id,
                "user_id": new_schedule.user_id,
                "subject_id": new_schedule.subject_id,
                "classroom_id": new_schedule.classroom_id,
                "date": new_schedule.date.isoformat(),
                "start": str(new_schedule.start),
                "end": str(new_schedule.end),
            }), 201)

        except Exception as e:
            return make_response(jsonify({"error": str(e)}), 500)
