import uuid
from sqlalchemy import UUID, Column, String, DateTime
from datetime import datetime, timezone
from sqlalchemy.orm import relationship
from models.base import Base

class User(Base):
    __tablename__ = 'user'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(120), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    created_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    # role = Column(String(50), nullable=False)
    schedules = relationship(
        'Schedule',
        back_populates='user',
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f'<User {self.email}>'
