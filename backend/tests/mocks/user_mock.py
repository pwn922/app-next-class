import uuid
from datetime import datetime, timezone
from unittest.mock import MagicMock
from models.user import User

def create_mock_user(
    id=None,
    email="test@example.com",
    password="hashed_password_123",
    created_at=None
):
    mock_user = MagicMock(spec=User)
    mock_user.id = id or uuid.uuid4()
    mock_user.email = email
    mock_user.password = password
    mock_user.created_at = created_at or datetime.now(timezone.utc)
    mock_user.schedules = []
    return mock_user