
from flask_restful import Resource, reqparse
from flask import jsonify, make_response
from flask_restful import Resource
from flasgger.utils import swag_from

class LoginResource(Resource):
    @swag_from("../docs/login/post.yml")
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('email', type=str, required=True)
        args = parser.parse_args()

        email = args.get('email')
        print(email)
        token_obj = {"token": '<token>'}
        return make_response(jsonify(token_obj), 200)


class LoginCallbackResource(Resource):
    pass