import uuid
from flask_restful import Resource, request
from flasgger.utils import swag_from
from flask import jsonify, make_response
from models.subject import Subject
from models.base import db

class SubjectListResource(Resource):
    @swag_from('../docs/subjects/get_all.yml')
    def get(self):
        try:
            subjects = db.session.query(Subject).all()
            result = [
                {"id": str(s.id), "name": s.name, "code": s.code}
                for s in subjects
            ]
            return make_response(jsonify(result), 200)
        except Exception as e:
            return make_response(jsonify({"error": str(e)}), 500)

    @swag_from('../docs/subjects/post.yml')
    def post(self):
        try:
            data = request.json
            name = data.get("name")
            code = data.get("code")

            if not name or not code:
                return make_response(jsonify({"error": "Missing required fields."}), 400)

            new_subject = Subject(id=uuid.uuid4(), name=name, code=code)
            db.session.add(new_subject)
            db.session.commit()

            return make_response(jsonify({
                "id": str(new_subject.id),
                "name": new_subject.name,
                "code": new_subject.code
            }), 201)

        except Exception as e:
            return make_response(jsonify({"error": str(e)}), 500)

class SubjectResource(Resource):
    @swag_from('../docs/subjects/get.yml')
    def get(self, id):
        try:
            subject = db.session.query(Subject).filter_by(id=id).first()
            if not subject:
                return make_response(jsonify({"error": "Subject not found."}), 404)

            return make_response(jsonify({
                "id": str(subject.id),
                "name": subject.name,
                "code": subject.code
            }), 200)
        except Exception as e:
            return make_response(jsonify({"error": str(e)}), 500)

    @swag_from('../docs/subjects/put.yml')
    def put(self, id):
        try:
            subject = db.session.query(Subject).filter_by(id=id).first()
            if not subject:
                return make_response(jsonify({"error": "Subject not found."}), 404)

            data = request.json
            subject.name = data.get("name", subject.name)
            subject.code = data.get("code", subject.code)

            db.session.commit()

            return make_response(jsonify({
                "id": str(subject.id),
                "name": subject.name,
                "code": subject.code
            }), 200)

        except Exception as e:
            return make_response(jsonify({"error": str(e)}), 500)

    @swag_from('../docs/subjects/delete.yml')
    def delete(self, id):
        try:
            subject = db.session.query(Subject).filter_by(id=id).first()
            if not subject:
                return make_response(jsonify({"error": "Subject not found."}), 404)

            db.session.delete(subject)
            db.session.commit()
            return make_response('', 204)

        except Exception as e:
            return make_response(jsonify({"error": str(e)}), 500)
