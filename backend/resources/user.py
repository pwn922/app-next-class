import uuid
from flask_restful import Resource, reqparse, request
from flasgger.utils import swag_from
from flask import jsonify, make_response
from models.base import db
from models.user import User

class UserResource(Resource):
    @swag_from('../docs/users/get.yml')
    def get(self, user_id):
        try:
            user = db.session.query(User).filter_by(id=user_id).first()
            if not user:
                return make_response(jsonify({"error": 'User not found.'}), 404)

            user_obj = {"id": user.id, "name": user.name, "email": user.email}
            return make_response(jsonify(user_obj), 200)

        except Exception as e:
            return make_response(jsonify({"error": str(e)}), 500)
        
    #def put(self, user_id):
     #   pass

    #def delete(self, user_id):
    # pass

    @swag_from('../docs/users/put.yml')
    def put(self, user_id):
        try:
            user = db.session.query(User).filter_by(id=user_id).first()
            if not user:
                return make_response(jsonify({"error": 'User not found.'}), 404)

            data = request.json
            name = data.get("name")
            email = data.get("email")

            if name:
                user.name = name
            if email:
                user.email = email

            db.session.commit()

            return make_response(jsonify({
                "id": user.id,
                "name": user.name,
                "email": user.email
            }), 200)

        except Exception as e:
            return make_response(jsonify({"error": str(e)}), 500)

    @swag_from('../docs/users/delete.yml')
    def delete(self, user_id):
        try:
            user = db.session.query(User).filter_by(id=user_id).first()
            if not user:
                return make_response(jsonify({"error": 'User not found.'}), 404)

            db.session.delete(user)
            db.session.commit()

            return make_response('', 204)

        except Exception as e:
            return make_response(jsonify({"error": str(e)}), 500)

class UserListResource(Resource):
    def get(self):
        pass
        # user_data = {"user_id": "1", "username": "example_user", "email": "user@example.com"}
        # return jsonify(user_data), 200

    @swag_from("../docs/users/get_all.yml")
    def get(self):
        try:
            users = db.session.query(User).all()
            result = [
                {"id": str(user.id), "name": user.name, "email": user.email}
                for user in users
            ]
            return make_response(jsonify(result), 200)
        except Exception as e:
            return make_response(jsonify({"error": str(e)}), 500)

    @swag_from("../docs/users/post.yml")
    def post(self):
        try:
            data = request.json

            # Validación simple
            name = data.get("name")
            email = data.get("email")
            password = data.get("password")

            #Si no encuentra un campo de los requeridos, devolverá error de tipo 400
            if not name or not email or not password:
                return make_response(jsonify({"error": "Missing required fields."}), 400)

            # Crear y guardar el nuevo usuario
            new_user = User(
                id=uuid.uuid4(),
                name=name,
                email=email,
                password=password
            )

            db.session.add(new_user)
            db.session.commit()

            return make_response(jsonify({
                "id": str(new_user.id),
                "name": new_user.name,
                "email": new_user.email
            }), 201)

        except Exception as e:
            return make_response(jsonify({"error": str(e)}), 500)

        