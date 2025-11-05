"""Utility functions for bot handlers."""

import logging
from typing import Optional
from telegram import Update
from telegram.ext import ContextTypes

from models import User
from config.database import SessionLocal

logger = logging.getLogger(__name__)


def get_user_from_update(update: Update) -> Optional[User]:
    """
    Get User object from database based on update.
    
    Args:
        update: Telegram update object
    
    Returns:
        User object or None
    """
    if not update.effective_user:
        return None
    
    user_id = update.effective_user.id
    
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.user_id == user_id).first()
        return user
    finally:
        db.close()


def format_price(amount: float, currency: str = "ETB") -> str:
    """
    Format price with currency.
    
    Args:
        amount: Price amount
        currency: Currency code
    
    Returns:
        Formatted price string
    """
    if currency == "ETB":
        return f"{amount:,.2f} Birr"
    elif currency == "USD":
        return f"${amount:,.2f}"
    else:
        return f"{amount:,.2f} {currency}"


def truncate_text(text: str, max_length: int = 100) -> str:
    """
    Truncate text to max length.
    
    Args:
        text: Text to truncate
        max_length: Maximum length
    
    Returns:
        Truncated text
    """
    if len(text) <= max_length:
        return text
    return text[:max_length - 3] + "..."


