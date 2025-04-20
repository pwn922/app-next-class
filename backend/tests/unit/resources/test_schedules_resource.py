import json
from unittest.mock import patch

from flask_jwt_extended import create_access_token

from responses.schedules_response import ScheduleSuccessResponse
from tests.mocks.schedule_mock import create_mock_schedule_list

class TestSchedulesResource:
    @patch('database.db.db.session')
    def test_get_schedules(self, mock_db_session, client, app):
        user_id = "123e4567-e89b-12d3-a456-426614174000"
        access_token = create_access_token(identity=user_id)
        headers = {
            "Authorization": f"Bearer {access_token}"
        }

        mock_db_session.query().filter_by().scalar.return_value = None
        mock_schedule_list = create_mock_schedule_list(day="lunes", user_id=user_id)
        mock_db_session.query.return_value.filter_by.return_value.all.return_value = mock_schedule_list

        response = client.get('/api/v1/user/schedules/', headers=headers)
        data = json.loads(response.data.decode())

        assert response.status_code == ScheduleSuccessResponse.LIST_RETRIEVED.value.get("status_code")
        assert data['success'] is True
        assert len(data['data']) == 2
        assert data['data'][0]['day'] == "lunes"
        assert data['data'][1]['day'] == "lunes"