

from datetime import datetime
from datetime import timezone
import logging


from models.token_blocklist import TokenBlocklist
from database.db import db

from flask import jsonify, make_response
from flask_jwt_extended import get_jwt, jwt_required
from flask_restful import Resource


from auth import jwt_auth

logging.basicConfig(level=logging.INFO)

# TODO - MEJORAR LOS MENSAJES

LOGOUT_SUCCESS = {"success": True, "message": "Logout successful.", "data": {}}

@jwt_auth.jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_payload):
    jti = jwt_payload.get("jti")
    token = db.session.query(TokenBlocklist.id).filter_by(jti=jti).scalar()
    return token is not None

class LogoutResource(Resource):
    @jwt_required()
    def post(self):
        jti = get_jwt().get("jti")
        logging.info(f"Logout - Jti: {jti}")
        _type = get_jwt().get("type")
        now = datetime.now(timezone.utc)
        db.session.add(TokenBlocklist(jti=jti, type=_type, created_at=now))
        db.session.commit()
        return make_response(jsonify(LOGOUT_SUCCESS), 200)