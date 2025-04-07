from sqlalchemy import UUID, Column, Integer, String
from sqlalchemy.orm import relationship
from models.base import Base

class Pavilion(Base):
    __tablename__ = 'pavilion'
    id = Column(UUID(as_uuid=True), primary_key=True)
    name = Column(String(100), nullable=False)

    #Relación entre un pabellón y sus salas de clases.
    classrooms = relationship('Classroom', back_populates='pavilion', cascade="all, delete-orphan")

    def __repr__(self):
        return f'<Classroom {self.name}>'
