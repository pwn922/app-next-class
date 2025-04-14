from sqlalchemy import UUID, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from models.base import Base
import uuid


class Schedule(Base):
    __tablename__ = 'schedule'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    pavilion = Column(String(100), nullable=False)
    block = Column(String(10), nullable=False)
    classroom = Column(Integer, nullable=False)
    day = Column(String(20), nullable=False)
    subject = Column(String(100), nullable=False)
    created_at = Column(
        DateTime,
        default=datetime.now(timezone.utc),
        nullable=False
    )

    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey('user.id', ondelete="CASCADE"),
        nullable=True
    )
    user = relationship("User", back_populates="schedules")

    def __repr__(self):
        return f'<Schedule {self.id} {self.day} {self.block} {self.subject}>'
