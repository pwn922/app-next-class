

import json
from unittest.mock import patch

from flask_jwt_extended import create_access_token

from responses.logout_response import LogoutSuccessResponse


class TestLogoutResource:
    @patch('database.db.db.session')
    def test_logout(self, mock_db_session, client):
        access_token = create_access_token(identity="user123", additional_claims={"type": "access"})
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