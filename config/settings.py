"""Configuration settings for Trip Ethiopia Bot."""

import os
from typing import List
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Settings:
    """Application settings loaded from environment variables."""

    # Telegram Bot
    TELEGRAM_BOT_TOKEN: str = os.getenv("TELEGRAM_BOT_TOKEN", "")

    # Database
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "postgresql://user:password@localhost:5432/trip_ethiopia"
    )

    # Trip.com API
    TRIP_COM_API_KEY: str = os.getenv("TRIP_COM_API_KEY", "")
    TRIP_COM_API_SECRET: str = os.getenv("TRIP_COM_API_SECRET", "")
    TRIP_COM_BASE_URL: str = os.getenv(
        "TRIP_COM_BASE_URL",
        "https://api.trip.com"
    )

    # Currency API
    CURRENCY_API_KEY: str = os.getenv("CURRENCY_API_KEY", "")
    CURRENCY_API_URL: str = os.getenv(
        "CURRENCY_API_URL",
        "https://api.exchangerate.host"
    )

    # Payment Gateways
    TELEBIRR_API_KEY: str = os.getenv("TELEBIRR_API_KEY", "")
    TELEBIRR_API_SECRET: str = os.getenv("TELEBIRR_API_SECRET", "")
    TELEBIRR_API_URL: str = os.getenv("TELEBIRR_API_URL", "")

    CBE_BIRR_API_KEY: str = os.getenv("CBE_BIRR_API_KEY", "")
    CBE_BIRR_API_SECRET: str = os.getenv("CBE_BIRR_API_SECRET", "")
    CBE_BIRR_API_URL: str = os.getenv("CBE_BIRR_API_URL", "")

    # Redis
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")

    # Application Settings
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    DEBUG: bool = os.getenv("DEBUG", "True").lower() == "true"

    # Admin Users
    ADMIN_USER_IDS: List[int] = [
        int(uid.strip()) for uid in os.getenv("ADMIN_USER_IDS", "").split(",")
        if uid.strip()
    ]

    # Currency Settings
    DEFAULT_CURRENCY: str = os.getenv("DEFAULT_CURRENCY", "ETB")
    USD_TO_ETB_RATE: float = float(os.getenv("USD_TO_ETB_RATE", "55.5"))

    # PDF Generation
    TICKET_LOGO_PATH: str = os.getenv("TICKET_LOGO_PATH", "assets/logo.png")
    COMPANY_NAME: str = os.getenv("COMPANY_NAME", "Trip Ethiopia")
    COMPANY_EMAIL: str = os.getenv(
        "COMPANY_EMAIL",
        "support@tripethiopia.com"
    )
    COMPANY_PHONE: str = os.getenv("COMPANY_PHONE", "+251911234567")

    # Notification Settings
    ENABLE_PRICE_ALERTS: bool = os.getenv(
        "ENABLE_PRICE_ALERTS",
        "True"
    ).lower() == "true"
    PRICE_CHECK_INTERVAL: int = int(os.getenv("PRICE_CHECK_INTERVAL", "3600"))
    REMINDER_HOURS_BEFORE_FLIGHT: int = int(
        os.getenv("REMINDER_HOURS_BEFORE_FLIGHT", "24")
    )

    # Bot Settings
    MAX_SEARCH_RESULTS: int = int(os.getenv("MAX_SEARCH_RESULTS", "10"))
    SESSION_TIMEOUT: int = int(os.getenv("SESSION_TIMEOUT", "1800"))

    # Supported Languages
    SUPPORTED_LANGUAGES: List[str] = ["en", "am", "om"]
    DEFAULT_LANGUAGE: str = "en"

    def validate(self) -> bool:
        """Validate required settings."""
        if not self.TELEGRAM_BOT_TOKEN:
            raise ValueError("TELEGRAM_BOT_TOKEN is required")
        return True


# Create global settings instance
settings = Settings()


