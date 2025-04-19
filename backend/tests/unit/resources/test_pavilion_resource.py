import json
from unittest.mock import patch
from tests.mocks.pavilion_mock import create_mock_pavilion, create_mock_pavilion_list


class TestPavilionResource:
    @patch('database.db.db.session')
    def test_get_pavilion_success(self, mock_db_session, client):
        mock_pavilion = create_mock_pavilion()
        mock_db_session.query.return_value.filter_by.return_value.first.return_value = mock_pavilion

        response = client.get(f'/api/v1/pavilions/{mock_pavilion.id}')
        data = json.loads(response.data.decode())

        assert response.status_code == 200
        assert data['success'] is True
        assert data['data']['name'] == mock_pavilion.name
        assert data['data']['x'] == mock_pavilion.x
        assert data['data']['y'] == mock_pavilion.y

    