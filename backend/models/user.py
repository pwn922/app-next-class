import uuid
from sqlalchemy import UUID, Column, Integer, String

from sqlalchemy import UUID, Column, Integer, String, DateTime
from datetime import datetime, timezone
from sqlalchemy.orm import relationship
from models.base import Base

class User(Base):
    __tablename__ = 'users'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4())
    google_id = Column(String(255), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    password = Column(String(255), nullable =False)
    created_at = Column(DateTime, default=datetime.now(timezone.utc), nullable=False)

    #Relacion entre el Usuario y el Horario
    schedules = relationship('Schedule', back_populates='user', cascade="all, delete-orphan")
    #role = Column(String(50), nullable=False)

    def __repr__(self):
        return f'<User {self.email}>'