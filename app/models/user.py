from sqlalchemy import Column, Integer, DateTime, String
from sqlalchemy.sql import func
from app.database import Base
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    github_username = Column(String, unique=True, index=True, nullable=True)
    email = Column(String, unique=True, index=True, nullable=True)
    github_access_token = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    github_events = relationship("GithubEvent", back_populates="user")