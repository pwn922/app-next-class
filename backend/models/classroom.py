from sqlalchemy import UUID, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from models.base import Base
from models.pavilion import Pavilion

class Classroom(Base):
    __tablename__ = 'classroom'
    id = Column(UUID(as_uuid=True), primary_key=True)
    number = Column(Integer, nullable=False)
    pavilion_id = Column(UUID(as_uuid=True), ForeignKey('pavilion.id', ondelete="CASCADE"), nullable=False)

    pavilion = relationship("Pavilion", back_populates="classrooms")
    schedules = relationship('Schedule', back_populates='classroom', cascade="all, delete-orphan")

    def __repr__(self):
        return f'<Classroom {self.number} (ID: {self.id})>'

