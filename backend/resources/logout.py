from datetime import datetime, timezone
import logging

from flask_jwt_extended import get_jwt, jwt_required
from flask_restful import Resource

from models.token_blocklist import TokenBlocklist
from database.db import db
from auth import jwt_auth
from utils.responses import success_response, error_response
from responses.logout_response import (
    LogoutSuccessResponse,
    LogoutErrorResponse
)

logging.basicConfig(level=logging.INFO)


@jwt_auth.jwt.token_in_blocklist_loader
def check_if_token_revoked(_, jwt_payload):
    jti = jwt_payload.get("jti")
    token = db.session.query(TokenBlocklist.id).filter_by(jti=jti).scalar()
    return token is not None


class LogoutResource(Resource):
    @jwt_required()
    def post(self):
        try:
            jti = get_jwt().get("jti")
            logging.info(f"Logout - JTI: {jti}")
            _type = get_jwt().get("type")
            now = datetime.now(timezone.utc)

            db.session.add(TokenBlocklist(jti=jti, type=_type, created_at=now))
            db.session.commit()

            return success_response(
                message_key=LogoutSuccessResponse.LOGOUT_SUCCESS.value
                .get("message"),
                status_code=LogoutSuccessResponse.LOGOUT_SUCCESS.value
                .get("status_code")
            )

        except Exception as e:
            logging.error(f"Unexpected error during post logout: {e}")
            return error_response(
                error_code=LogoutErrorResponse.UNEXPECTED_ERROR.name,
                status_code=LogoutErrorResponse.UNEXPECTED_ERROR.value
                .get("status_code"),
                message=LogoutErrorResponse.UNEXPECTED_ERROR.value
                .get("message")
            )
