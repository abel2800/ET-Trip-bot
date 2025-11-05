"""Input validation utilities."""

import re
from datetime import datetime
from typing import Optional, Tuple


def validate_date(date_str: str) -> Tuple[bool, Optional[datetime]]:
    """
    Validate date string in YYYY-MM-DD format.
    
    Args:
        date_str: Date string to validate
    
    Returns:
        Tuple of (is_valid, datetime_object or None)
    """
    try:
        date_obj = datetime.strptime(date_str, "%Y-%m-%d")
        # Check if date is in the future
        if date_obj.date() < datetime.now().date():
            return False, None
        return True, date_obj
    except ValueError:
        return False, None


def validate_number(number_str: str, min_value: int = 1, max_value: int = None) -> Tuple[bool, Optional[int]]:
    """
    Validate if string is a valid number within range.
    
    Args:
        number_str: Number string to validate
        min_value: Minimum allowed value
        max_value: Maximum allowed value (optional)
    
    Returns:
        Tuple of (is_valid, number or None)
    """
    try:
        number = int(number_str)
        if number < min_value:
            return False, None
        if max_value is not None and number > max_value:
            return False, None
        return True, number
    except ValueError:
        return False, None


def validate_email(email: str) -> bool:
    """
    Validate email address format.
    
    Args:
        email: Email string to validate
    
    Returns:
        True if valid, False otherwise
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def validate_phone(phone: str) -> bool:
    """
    Validate Ethiopian phone number.
    
    Args:
        phone: Phone number string
    
    Returns:
        True if valid, False otherwise
    """
    # Ethiopian phone numbers: +251XXXXXXXXX or 0XXXXXXXXX
    pattern = r'^(\+251|0)[79]\d{8}$'
    return bool(re.match(pattern, phone.replace(" ", "").replace("-", "")))


def validate_city(city: str) -> Tuple[bool, Optional[str]]:
    """
    Validate and normalize city name.
    
    Args:
        city: City name to validate
    
    Returns:
        Tuple of (is_valid, normalized_city or None)
    """
    if not city or len(city) < 2:
        return False, None
    
    # Capitalize first letter of each word
    normalized = city.strip().title()
    return True, normalized


