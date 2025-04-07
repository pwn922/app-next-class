from sqlalchemy import Column, Integer, String, DateTime

from models.base import Base

class TokenBlocklist(Base):
    __tablename__ = 'token_blocklist'

    id = Column(Integer, primary_key=True)
    jti = Column(String(36), nullable=False, index=True)
    type = Column(String(16), nullable=False)
    created_at = Column(DateTime, nullable=False)
