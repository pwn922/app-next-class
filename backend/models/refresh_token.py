import uuid
from sqlalchemy import UUID, Column, ForeignKey, String
from models.base import Base
from sqlalchemy.orm import relationship

class RefreshToken(Base):
    __tablename__ = 'refresh_tokens'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    token = Column(String(500), nullable=False, unique=True)
    user_google_id = Column(String(255), ForeignKey('user.google_id'), nullable=False)
    user = relationship("User", backref="refresh_tokens")
    
    def __repr__(self):
        return f'<RefreshToken email={self.email}>'