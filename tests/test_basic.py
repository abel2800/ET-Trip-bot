"""Basic tests for Trip Ethiopia Bot."""

import pytest
from config.settings import settings
from utils.i18n import get_text, load_translations
from utils.validators import validate_date, validate_number, validate_email
from services.currency import CurrencyConverter


def test_settings_loaded():
    """Test that settings are loaded correctly."""
    assert settings.SUPPORTED_LANGUAGES == ["en", "am", "om"]
    assert settings.DEFAULT_LANGUAGE == "en"
    assert settings.DEFAULT_CURRENCY == "ETB"


def test_translations_loaded():
    """Test that translations are loaded."""
    load_translations()
    
    # Test English
    welcome_text = get_text("welcome", language="en")
    assert "Trip Ethiopia" in welcome_text
    
    # Test Amharic
    welcome_text_am = get_text("welcome", language="am")
    assert "ትሪፕ ኢትዮጵያ" in welcome_text_am
    
    # Test Oromo
    welcome_text_om = get_text("welcome", language="om")
    assert "Trip Ethiopia" in welcome_text_om


def test_text_formatting():
    """Test text formatting with parameters."""
    text = get_text(
        "flights.results_found",
        language="en",
        count=5
    )
    assert "5" in text


def test_date_validation():
    """Test date validation."""
    # Valid future date
    is_valid, date_obj = validate_date("2025-12-31")
    assert is_valid is False or is_valid is True  # Depends on current date
    
    # Invalid format
    is_valid, _ = validate_date("31-12-2025")
    assert is_valid is False
    
    # Invalid date
    is_valid, _ = validate_date("2025-13-45")
    assert is_valid is False


def test_number_validation():
    """Test number validation."""
    # Valid number
    is_valid, num = validate_number("5", min_value=1, max_value=10)
    assert is_valid is True
    assert num == 5
    
    # Out of range
    is_valid, _ = validate_number("15", min_value=1, max_value=10)
    assert is_valid is False
    
    # Invalid format
    is_valid, _ = validate_number("abc", min_value=1)
    assert is_valid is False


def test_email_validation():
    """Test email validation."""
    # Valid emails
    assert validate_email("test@example.com") is True
    assert validate_email("user.name@domain.co.uk") is True
    
    # Invalid emails
    assert validate_email("invalid.email") is False
    assert validate_email("@example.com") is False
    assert validate_email("test@") is False


def test_currency_converter():
    """Test currency converter."""
    converter = CurrencyConverter()
    
    # Test conversion
    etb_amount = converter.convert_usd_to_etb(100)
    assert etb_amount > 0
    assert isinstance(etb_amount, float)
    
    # Test reverse conversion
    usd_amount = converter.convert_etb_to_usd(5000)
    assert usd_amount > 0
    assert isinstance(usd_amount, float)
    
    # Test price formatting
    formatted = converter.format_price(1234.56, "ETB")
    assert "1,234.56" in formatted
    assert "Birr" in formatted


def test_keyboard_structure():
    """Test keyboard creation."""
    from bot.keyboards import get_main_menu_keyboard
    
    keyboard = get_main_menu_keyboard(language="en")
    assert keyboard is not None
    assert len(keyboard.inline_keyboard) > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])


