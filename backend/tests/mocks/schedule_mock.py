

from datetime import datetime
from datetime import timedelta
from datetime import timezone
from unittest.mock import MagicMock
import uuid


def create_mock_schedule(
    id=None,
    pavilion="PABELLON A",
    block="B1",
    classroom=101,
    day="monday",
    subject="Matemáticas",
    user_id=None
):
    mock_schedule = MagicMock()
    mock_schedule.id = id or uuid.uuid4()
    mock_schedule.pavilion = pavilion
    mock_schedule.block = block
    mock_schedule.classroom = classroom
    mock_schedule.day = day
    mock_schedule.subject = subject
    mock_schedule.user_id = user_id or uuid.uuid4()
    return mock_schedule

def create_mock_schedule_list(
    pavilion="PABELLON A",
    block="B1",
    classroom=101,
    day="monday",
    subject="Matemáticas",
    user_id=None
):
    mock_schedule_1 = create_mock_schedule(
        pavilion=pavilion,
        block=block,
        classroom=classroom,
        day=day,
        subject=subject,
        user_id=user_id
    )
    mock_schedule_2 = create_mock_schedule(
        pavilion=pavilion,
        block=block,
        classroom=classroom,
        day=day,
        subject=subject,
        user_id=user_id
    )
    return [mock_schedule_1, mock_schedule_2]