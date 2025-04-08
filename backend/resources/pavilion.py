import uuid
from flask_restful import Resource, request
from flasgger.utils import swag_from
from flask import jsonify, make_response
from models.base import db
from models.pavilion import Pavilion

class PavilionListResource(Resource):
    @swag_from('../docs/pavilions/get_all.yml')
    def get(self):
        try:
            pavilions = db.session.query(Pavilion).all()
            result = [{"id": str(p.id), "name": p.name} for p in pavilions]
            return make_response(jsonify(result), 200)
        except Exception as e:
            return make_response(jsonify({"error": str(e)}), 500)

    @swag_from('../docs/pavilions/post.yml')
    def post(self):
        try:
            data = request.get_json()
            name = data.get("name")

            if not name:
                return make_response(jsonify({"error": "Missing 'name' field"}), 400)

            new_pavilion = Pavilion(id=uuid.uuid4(), name=name)
            db.session.add(new_pavilion)
            db.session.commit()

            return make_response(jsonify({
                "id": str(new_pavilion.id),
                "name": new_pavilion.name
            }), 201)

        except Exception as e:
            return make_response(jsonify({"error": str(e)}), 500)


class PavilionResource(Resource):
    @swag_from('../docs/pavilions/get.yml')
    def get(self, id):
        try:
            pavilion = db.session.query(Pavilion).filter_by(id=id).first()
            if not pavilion:
                return make_response(jsonify({"error": "Pavilion not found"}), 404)

            return make_response(jsonify({
                "id": str(pavilion.id),
                "name": pavilion.name
            }), 200)
        except Exception as e:
            return make_response(jsonify({"error": str(e)}), 500)

    @swag_from('../docs/pavilions/put.yml')
    def put(self, id):
        try:
            data = request.get_json()
            name = data.get("name")

            pavilion = db.session.query(Pavilion).filter_by(id=id).first()
            if not pavilion:
                return make_response(jsonify({"error": "Pavilion not found"}), 404)

            if name:
                pavilion.name = name

            db.session.commit()

            return make_response(jsonify({
                "id": str(pavilion.id),
                "name": pavilion.name
            }), 200)

        except Exception as e:
            return make_response(jsonify({"error": str(e)}), 500)

    @swag_from('../docs/pavilions/delete.yml')
    def delete(self, id):
        try:
            pavilion = db.session.query(Pavilion).filter_by(id=id).first()
            if not pavilion:
                return make_response(jsonify({"error": "Pavilion not found"}), 404)

            db.session.delete(pavilion)
            db.session.commit()

            return make_response('', 204)

        except Exception as e:
            return make_response(jsonify({"error": str(e)}), 500)
