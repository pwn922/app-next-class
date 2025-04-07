from flask_jwt_extended import jwt_required
from flask_restful import Resource


class RefreshTokenResource(Resource):
    @jwt_required()
    def post(self):
        pass