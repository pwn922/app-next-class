from sqlalchemy import UUID, Column, String, Float
from sqlalchemy.orm import relationship
from models.base import Base


class Pavilion(Base):
    __tablename__ = 'pavilion'
    id = Column(UUID(as_uuid=True), primary_key=True)
    name = Column(String(100), nullable=False)
    x = Column(Float, nullable=False)
    y = Column(Float, nullable=False)

    def __repr__(self):
        return f'<Pavilion {self.name}>'
