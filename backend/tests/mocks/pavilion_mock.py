import uuid
from unittest.mock import MagicMock
from models.pavilion import Pavilion

def create_mock_pavilion(
    id=None,
    name="Test Pavilion",
    x=10.0,
    y=20.0
):
    """Creates a mock Pavilion instance"""
    mock_pavilion = MagicMock(spec=Pavilion)
    mock_pavilion.id = id or uuid.uuid4()
    mock_pavilion.name = name
    mock_pavilion.x = x
    mock_pavilion.y = y
    return mock_pavilion

def create_mock_pavilion_list():
    """Creates a list of mock Pavilion instances"""
    return [
        create_mock_pavilion(name="Pavilion A", x=10.0, y=20.0),
        create_mock_pavilion(name="Pavilion B", x=30.0, y=40.0),
        create_mock_pavilion(name="Pavilion C", x=50.0, y=60.0)
    ]