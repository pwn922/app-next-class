from sqlalchemy import UUID, Column, Integer, String

from models.base import Base

class Classroom(Base):
    __tablename__ = 'classroom'
    _id = Column(UUID(as_uuid=True), primary_key=True)
    number = Column(Integer, nullable=False)

    def __repr__(self):
        return f'<Classroom {self.name}>'
