"""
from sqlalchemy import UUID, Column, Integer, String
from sqlalchemy.orm import relationship
from models.base import Base

class Subject(Base):
    __tablename__ = 'subject'
    id = Column(UUID(as_uuid=True), primary_key=True)
    name = Column(String(50), nullable=False)
    code = Column(String(120), nullable=False)

    #Relación entre una asignatura y un horario.
    schedules = relationship('Schedule', back_populates='subject', cascade="all, delete-orphan")

    def __repr__(self):
        return f'<Classroom {self.name}>'

"""  