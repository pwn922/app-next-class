import uuid
from flask_restful import Resource, request
from flasgger.utils import swag_from
from flask import jsonify, make_response
from database.db import db
from models.classroom import Classroom

class ClassroomResource(Resource):
    @swag_from('../docs/classrooms/get.yml')
    def get(self, id):
        try:
            classroom = db.session.query(Classroom).filter_by(id=id).first()
            if not classroom:
                return make_response(jsonify({"error": "Classroom not found"}), 404)
            
            classroom_data = {
                "id": classroom.id,
                "number": classroom.number,
                "pavilion_id": classroom.pavilion_id
            }
            return make_response(jsonify(classroom_data), 200)
        except Exception as e:
            return make_response(jsonify({"error": str(e)}), 500)

    @swag_from('../docs/classrooms/put.yml')
    def put(self, id):
        try:
            classroom = db.session.query(Classroom).filter_by(id=id).first()
            if not classroom:
                return make_response(jsonify({"error": "Classroom not found"}), 404)

            data = request.json
            classroom.number = data.get("number", classroom.number)
            classroom.pavilion_id = data.get("pavilion_id", classroom.pavilion_id)

            db.session.commit()
            updated = {
                "id": classroom.id,
                "number": classroom.number,
                "pavilion_id": classroom.pavilion_id
            }
            return make_response(jsonify(updated), 200)
        except Exception as e:
            return make_response(jsonify({"error": str(e)}), 500)

    @swag_from('../docs/classrooms/delete.yml')
    def delete(self, id):
        try:
            classroom = db.session.query(Classroom).filter_by(id=id).first()
            if not classroom:
                return make_response(jsonify({"error": "Classroom not found"}), 404)

            db.session.delete(classroom)
            db.session.commit()
            return make_response('', 204)
        except Exception as e:
            return make_response(jsonify({"error": str(e)}), 500)


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
            return make_response(jsonify(result), 200)
        except Exception as e:
            return make_response(jsonify({"error": str(e)}), 500)

    @swag_from('../docs/classrooms/post.yml')
    def post(self):
        try:
            data = request.json
            number = data.get("number")
            pavilion_id = data.get("pavilion_id")

            if number is None or pavilion_id is None:
                return make_response(jsonify({"error": "Missing required fields."}), 400)

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
            return make_response(jsonify(response), 201)
        except Exception as e:
            return make_response(jsonify({"error": str(e)}), 500)
