

from datetime import timedelta
import json
from unittest.mock import patch

from flask_jwt_extended import create_access_token

from responses.logout_response import LogoutSuccessResponse


class TestLogoutResource:
    @patch('database.db.db.session')
    def test_logout(self, mock_db_session, client):
        user_id = "123e4567-e89b-12d3-a456-426614174000"
        mock_db_session.query().filter_by().scalar.return_value = None
        access_token_expires = timedelta(hours=1)
        access_token = create_access_token(identity=user_id, expires_delta=access_token_expires, additional_claims={"type": "access"})
        headers = {
            "Authorization": f"Bearer {access_token}"
        }

        response = client.post('/api/v1/logout', headers=headers)
        data = json.loads(response.data.decode())
        
        assert response.status_code == LogoutSuccessResponse.LOGOUT_SUCCESS.value.get("status_code")
        assert data["success"] is True
        assert data["message"] == LogoutSuccessResponse.LOGOUT_SUCCESS.value.get("message")

        mock_db_session.add.assert_called_once()
        mock_db_session.commit.assert_called_once()