"""User model for storing Telegram user information."""

from sqlalchemy import Column, BigInteger, String, DateTime, func
from config.database import Base


class User(Base):
    """User model representing a Telegram user."""

    __tablename__ = "users"

    user_id = Column(BigInteger, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    language = Column(String(10), default="en", nullable=False)
    email = Column(String(255), nullable=True)
    phone = Column(String(50), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )

    def __repr__(self):
        return f"<User(user_id={self.user_id}, name='{self.name}', language='{self.language}')>"

    def to_dict(self):
        """Convert user object to dictionary."""
        return {
            "user_id": self.user_id,
            "name": self.name,
            "language": self.language,
            "email": self.email,
            "phone": self.phone,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }


