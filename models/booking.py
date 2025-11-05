"""Booking model for storing user bookings."""

from sqlalchemy import Column, Integer, BigInteger, String, Float, DateTime, Enum, JSON, ForeignKey, func
from sqlalchemy.orm import relationship
import enum

from config.database import Base


class BookingType(enum.Enum):
    """Enum for booking types."""
    FLIGHT = "Flight"
    HOTEL = "Hotel"
    TOUR = "Tour"


class PaymentStatus(enum.Enum):
    """Enum for payment status."""
    PENDING = "Pending"
    COMPLETED = "Completed"
    FAILED = "Failed"
    REFUNDED = "Refunded"


class Booking(Base):
    """Booking model representing a user's travel booking."""

    __tablename__ = "bookings"

    booking_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey("users.user_id"), nullable=False, index=True)
    type = Column(Enum(BookingType), nullable=False)
    provider = Column(String(255), nullable=False)
    booking_reference = Column(String(100), unique=True, nullable=True)
    booking_data = Column(JSON, nullable=False)
    payment_status = Column(Enum(PaymentStatus), default=PaymentStatus.PENDING)
    payment_method = Column(String(50), nullable=True)
    payment_reference = Column(String(100), nullable=True)
    total_price = Column(Float, nullable=False)
    currency = Column(String(10), default="ETB")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )

    def __repr__(self):
        return (
            f"<Booking(booking_id={self.booking_id}, "
            f"user_id={self.user_id}, "
            f"type={self.type.value}, "
            f"status={self.payment_status.value})>"
        )

    def to_dict(self):
        """Convert booking object to dictionary."""
        return {
            "booking_id": self.booking_id,
            "user_id": self.user_id,
            "type": self.type.value,
            "provider": self.provider,
            "booking_reference": self.booking_reference,
            "booking_data": self.booking_data,
            "payment_status": self.payment_status.value,
            "payment_method": self.payment_method,
            "payment_reference": self.payment_reference,
            "total_price": self.total_price,
            "currency": self.currency,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }


