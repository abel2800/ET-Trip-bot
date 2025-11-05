"""Price alert model for monitoring price changes."""

from sqlalchemy import Column, Integer, BigInteger, String, Float, DateTime, JSON, ForeignKey, Enum, func
import enum

from config.database import Base


class AlertType(enum.Enum):
    """Enum for alert types."""
    FLIGHT = "Flight"
    HOTEL = "Hotel"


class AlertStatus(enum.Enum):
    """Enum for alert status."""
    ACTIVE = "Active"
    TRIGGERED = "Triggered"
    CANCELLED = "Cancelled"
    EXPIRED = "Expired"


class PriceAlert(Base):
    """Price alert model for tracking price drop notifications."""

    __tablename__ = "price_alerts"

    alert_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey("users.user_id"), nullable=False, index=True)
    type = Column(Enum(AlertType), nullable=False)
    search_params = Column(JSON, nullable=False)
    target_price = Column(Float, nullable=False)
    current_price = Column(Float, nullable=True)
    currency = Column(String(10), default="ETB")
    status = Column(Enum(AlertStatus), default=AlertStatus.ACTIVE)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    triggered_at = Column(DateTime(timezone=True), nullable=True)
    expires_at = Column(DateTime(timezone=True), nullable=True)

    def __repr__(self):
        return (
            f"<PriceAlert(alert_id={self.alert_id}, "
            f"user_id={self.user_id}, "
            f"type={self.type.value}, "
            f"status={self.status.value})>"
        )

    def to_dict(self):
        """Convert price alert object to dictionary."""
        return {
            "alert_id": self.alert_id,
            "user_id": self.user_id,
            "type": self.type.value,
            "search_params": self.search_params,
            "target_price": self.target_price,
            "current_price": self.current_price,
            "currency": self.currency,
            "status": self.status.value,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "triggered_at": self.triggered_at.isoformat() if self.triggered_at else None,
            "expires_at": self.expires_at.isoformat() if self.expires_at else None,
        }


