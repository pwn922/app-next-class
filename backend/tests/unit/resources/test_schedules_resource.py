import json
from unittest.mock import patch

from flask_jwt_extended import create_access_token

from responses.schedules_response import ScheduleSuccessResponse
from tests.mocks.schedule_mock import create_mock_schedule, create_mock_schedule_list

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


    @patch('database.db.db.session')  
    def test_get_schedules_empty(self, mock_db_session, client, app):
        user_id = "123e4567-e89b-12d3-a456-426614174000"  
        access_token = create_access_token(identity=user_id)  
        headers = {
            "Authorization": f"Bearer {access_token}"  
        }

        mock_db_session.query.return_value.filter_by.return_value.all.return_value = []

        response = client.get('/api/v1/user/schedules/', headers=headers)  
        data = json.loads(response.data.decode())  

        assert response.status_code == 200  
        assert data['success'] is True  
        assert len(data['data']) == 0


    @patch('database.db.db.session')
    def test_get_schedule_not_found(self, mock_db_session, client, app):
        user_id = "123e4567-e89b-12d3-a456-426614174000"
        schedule_id = "987e6543-e89b-12d3-a456-426614174001"  
        access_token = create_access_token(identity=user_id)
        headers = {
            "Authorization": f"Bearer {access_token}"
        }

        mock_db_session.query.return_value.filter_by.return_value.first.return_value = None  

        response = client.get(f'/api/v1/user/schedules/{schedule_id}', headers=headers)
        data = json.loads(response.data.decode())

        assert response.status_code == 404  
        assert data['success'] is False
        assert 'message' in data


    @patch('database.db.db.session')
    def test_create_schedule_missing_fields(self, mock_db_session, client, app):
        user_id = "123e4567-e89b-12d3-a456-426614174000"
        access_token = create_access_token(identity=user_id)
        headers = {
            "Authorization": f"Bearer {access_token}"
        }

        
        new_schedule = {
            "pavilion": "Pabellón A",
            "block": "B1",
            "classroom": 101,
            "day": "lunes",
            
        }

        response = client.post('/api/v1/user/schedules/', json={"schedules": [new_schedule]}, headers=headers)
        data = json.loads(response.data.decode())

        assert response.status_code == 400  
        assert data['success'] is False
        assert 'message' in data  


    @patch('database.db.db.session')
    def test_create_schedule_duplicate(self, mock_db_session, client, app):
        user_id = "123e4567-e89b-12d3-a456-426614174000"
        access_token = create_access_token(identity=user_id)
        headers = {
            "Authorization": f"Bearer {access_token}"
        }

        
        new_schedule = {
            "pavilion": "Pabellón A",
            "block": "B1",
            "classroom": 101,
            "day": "lunes",
            "subject": "Matemáticas"
        }

        
        mock_db_session.query.return_value.filter_by.return_value.first.return_value = create_mock_schedule(user_id=user_id, **new_schedule)

        response = client.post('/api/v1/user/schedules/', json={"schedules": [new_schedule]}, headers=headers)
        data = json.loads(response.data.decode())

        assert response.status_code == 400  
        assert data['success'] is False
        assert 'message' in data  



    