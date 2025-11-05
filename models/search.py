"""Search history model for storing user search queries."""

from sqlalchemy import Column, Integer, BigInteger, String, Date, DateTime, JSON, ForeignKey, Enum, func
import enum

from config.database import Base


class SearchType(enum.Enum):
    """Enum for search types."""
    FLIGHT = "Flight"
    HOTEL = "Hotel"
    TOUR = "Tour"


class SearchHistory(Base):
    """Search history model for tracking user searches."""

    __tablename__ = "search_history"

    search_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey("users.user_id"), nullable=False, index=True)
    search_type = Column(Enum(SearchType), nullable=False)
    from_city = Column(String(100), nullable=True)
    to_city = Column(String(100), nullable=True)
    depart_date = Column(Date, nullable=True)
    return_date = Column(Date, nullable=True)
    passengers = Column(Integer, nullable=True)
    rooms = Column(Integer, nullable=True)
    guests = Column(Integer, nullable=True)
    search_params = Column(JSON, nullable=False)
    results = Column(JSON, nullable=True)
    searched_at = Column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return (
            f"<SearchHistory(search_id={self.search_id}, "
            f"user_id={self.user_id}, "
            f"type={self.search_type.value})>"
        )

    def to_dict(self):
        """Convert search history object to dictionary."""
        return {
            "search_id": self.search_id,
            "user_id": self.user_id,
            "search_type": self.search_type.value,
            "from_city": self.from_city,
            "to_city": self.to_city,
            "depart_date": self.depart_date.isoformat() if self.depart_date else None,
            "return_date": self.return_date.isoformat() if self.return_date else None,
            "passengers": self.passengers,
            "rooms": self.rooms,
            "guests": self.guests,
            "search_params": self.search_params,
            "results": self.results,
            "searched_at": self.searched_at.isoformat() if self.searched_at else None,
        }


