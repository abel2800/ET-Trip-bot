"""Internationalization (i18n) utilities for multi-language support."""

import json
import os
from typing import Dict, Any
from pathlib import Path

# Global translations cache
_translations: Dict[str, Dict[str, Any]] = {}
_user_languages: Dict[int, str] = {}

# Path to locales directory
LOCALES_DIR = Path(__file__).parent.parent / "locales"


def load_translations():
    """Load all translation files into memory."""
    global _translations
    
    for locale_file in LOCALES_DIR.glob("*.json"):
        lang_code = locale_file.stem
        with open(locale_file, "r", encoding="utf-8") as f:
            _translations[lang_code] = json.load(f)
    
    print(f"Loaded translations for languages: {list(_translations.keys())}")


def set_user_language(user_id: int, language: str):
    """
    Set the language preference for a user.
    
    Args:
        user_id: Telegram user ID
        language: Language code (en, am, om)
    """
    _user_languages[user_id] = language


def get_user_language(user_id: int) -> str:
    """
    Get the language preference for a user.
    
    Args:
        user_id: Telegram user ID
    
    Returns:
        Language code (defaults to 'en')
    """
    return _user_languages.get(user_id, "en")


def get_text(key: str, user_id: int = None, language: str = None, **kwargs) -> str:
    """
    Get translated text for a given key.
    
    Args:
        key: Translation key (e.g., 'welcome' or 'flights.search_title')
        user_id: Optional Telegram user ID to get user's language preference
        language: Optional language code to override user preference
        **kwargs: Format parameters for the text
    
    Returns:
        Translated and formatted text
    """
    # Determine language
    if language is None:
        if user_id is not None:
            language = get_user_language(user_id)
        else:
            language = "en"
    
    # Fallback to English if language not found
    if language not in _translations:
        language = "en"
    
    # Navigate through nested keys
    text = _translations[language]
    for part in key.split("."):
        if isinstance(text, dict):
            text = text.get(part, key)
        else:
            return key
    
    # Format text with parameters
    if kwargs and isinstance(text, str):
        try:
            text = text.format(**kwargs)
        except KeyError:
            pass
    
    return text if isinstance(text, str) else key


def get_all_text(user_id: int = None, language: str = None) -> Dict[str, Any]:
    """
    Get all translations for a specific language.
    
    Args:
        user_id: Optional Telegram user ID
        language: Optional language code
    
    Returns:
        Dictionary of all translations
    """
    if language is None:
        if user_id is not None:
            language = get_user_language(user_id)
        else:
            language = "en"
    
    return _translations.get(language, _translations.get("en", {}))


# Initialize translations on import
if not _translations:
    load_translations()


