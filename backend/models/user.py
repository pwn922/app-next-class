from sqlalchemy import UUID, Column, Integer, String

from models.base import Base

class User(Base):
    __tablename__ = 'user'
    id = Column(UUID(as_uuid=True), primary_key=True)
    name = Column(String(50), nullable=False)
    email = Column(String(120), unique=True, nullable=False)

    def __repr__(self):
        return f'<user {self.name}>'
