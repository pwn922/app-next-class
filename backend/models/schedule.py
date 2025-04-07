from sqlalchemy import UUID, Column, Integer, String, DateTime, Time, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from models.base import Base


class Schedule(Base):
    __tablename__ = 'schedule'
    id = Column(UUID(as_uuid=True), primary_key=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey('user.id', ondelete="CASCADE"), nullable=False)
    subject_id = Column(UUID(as_uuid=True), ForeignKey('subject.id', ondelete="CASCADE"), nullable=False)
    classroom_id = Column(UUID(as_uuid=True), ForeignKey('classroom.id',ondelete="CASCADE"), nullable=False)
    date = Column(DateTime, default=datetime.now(timezone.utc), nullable=False)
    start = Column(Time, nullable=False)   # Hora de inicio
    end = Column(Time, nullable=False)     # Hora de término

    user = relationship('User', back_populates='schedules')
    subject = relationship('Subject', back_populates='schedules')
    classroom = relationship('Classroom', back_populates='schedules')

    def __repr__(self):
        return f'<Schedule {self.date} {self.start}-{self.end}>'