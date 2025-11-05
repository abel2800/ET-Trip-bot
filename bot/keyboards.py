"""Keyboard layouts for the Telegram bot."""

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from typing import List
from utils.i18n import get_text


def get_main_menu_keyboard(user_id: int = None, language: str = "en") -> InlineKeyboardMarkup:
    """
    Get main menu inline keyboard.
    
    Args:
        user_id: Telegram user ID
        language: User's language preference
    
    Returns:
        InlineKeyboardMarkup with main menu options
    """
    keyboard = [
        [
            InlineKeyboardButton(
                get_text("main_menu.flights", user_id=user_id, language=language),
                callback_data="menu_flights"
            ),
            InlineKeyboardButton(
                get_text("main_menu.hotels", user_id=user_id, language=language),
                callback_data="menu_hotels"
            )
        ],
        [
            InlineKeyboardButton(
                get_text("main_menu.tours", user_id=user_id, language=language),
                callback_data="menu_tours"
            ),
            InlineKeyboardButton(
                get_text("main_menu.bookings", user_id=user_id, language=language),
                callback_data="menu_bookings"
            )
        ],
        [
            InlineKeyboardButton(
                get_text("main_menu.alerts", user_id=user_id, language=language),
                callback_data="menu_alerts"
            ),
            InlineKeyboardButton(
                get_text("main_menu.language", user_id=user_id, language=language),
                callback_data="menu_language"
            )
        ],
        [
            InlineKeyboardButton(
                get_text("main_menu.help", user_id=user_id, language=language),
                callback_data="menu_help"
            )
        ]
    ]
    
    return InlineKeyboardMarkup(keyboard)


def get_language_keyboard() -> InlineKeyboardMarkup:
    """
    Get language selection inline keyboard.
    
    Returns:
        InlineKeyboardMarkup with language options
    """
    keyboard = [
        [InlineKeyboardButton("🇬🇧 English", callback_data="lang_en")],
        [InlineKeyboardButton("🇪🇹 አማርኛ (Amharic)", callback_data="lang_am")],
        [InlineKeyboardButton("🇪🇹 Afaan Oromoo (Oromo)", callback_data="lang_om")]
    ]
    
    return InlineKeyboardMarkup(keyboard)


def get_payment_keyboard(user_id: int = None, language: str = "en") -> InlineKeyboardMarkup:
    """
    Get payment method selection keyboard.
    
    Args:
        user_id: Telegram user ID
        language: User's language preference
    
    Returns:
        InlineKeyboardMarkup with payment options
    """
    keyboard = [
        [
            InlineKeyboardButton(
                get_text("payment.telebirr", user_id=user_id, language=language),
                callback_data="payment_telebirr"
            )
        ],
        [
            InlineKeyboardButton(
                get_text("payment.cbe", user_id=user_id, language=language),
                callback_data="payment_cbe"
            )
        ],
        [
            InlineKeyboardButton(
                get_text("buttons.cancel", user_id=user_id, language=language),
                callback_data="payment_cancel"
            )
        ]
    ]
    
    return InlineKeyboardMarkup(keyboard)


def get_back_button_keyboard(user_id: int = None, language: str = "en") -> InlineKeyboardMarkup:
    """
    Get back button keyboard.
    
    Args:
        user_id: Telegram user ID
        language: User's language preference
    
    Returns:
        InlineKeyboardMarkup with back button
    """
    keyboard = [
        [
            InlineKeyboardButton(
                get_text("buttons.back", user_id=user_id, language=language),
                callback_data="back_to_menu"
            )
        ]
    ]
    
    return InlineKeyboardMarkup(keyboard)


def get_confirm_cancel_keyboard(user_id: int = None, language: str = "en") -> InlineKeyboardMarkup:
    """
    Get confirm/cancel keyboard.
    
    Args:
        user_id: Telegram user ID
        language: User's language preference
    
    Returns:
        InlineKeyboardMarkup with confirm and cancel buttons
    """
    keyboard = [
        [
            InlineKeyboardButton(
                get_text("buttons.confirm", user_id=user_id, language=language),
                callback_data="confirm"
            ),
            InlineKeyboardButton(
                get_text("buttons.cancel", user_id=user_id, language=language),
                callback_data="cancel"
            )
        ]
    ]
    
    return InlineKeyboardMarkup(keyboard)


def get_ethiopian_cities_keyboard() -> ReplyKeyboardMarkup:
    """
    Get keyboard with major Ethiopian cities.
    
    Returns:
        ReplyKeyboardMarkup with city options
    """
    cities = [
        ["Addis Ababa", "Dire Dawa"],
        ["Mekele", "Gondar"],
        ["Bahir Dar", "Hawassa"],
        ["Jimma", "Adama"],
        ["Harar", "Axum"]
    ]
    
    return ReplyKeyboardMarkup(
        cities,
        one_time_keyboard=True,
        resize_keyboard=True
    )


def get_international_cities_keyboard() -> ReplyKeyboardMarkup:
    """
    Get keyboard with major international cities.
    
    Returns:
        ReplyKeyboardMarkup with city options
    """
    cities = [
        ["Dubai", "Istanbul"],
        ["London", "Paris"],
        ["New York", "Washington DC"],
        ["Cairo", "Nairobi"],
        ["Johannesburg", "Lagos"]
    ]
    
    return ReplyKeyboardMarkup(
        cities,
        one_time_keyboard=True,
        resize_keyboard=True
    )


def create_flight_result_keyboard(flights: List[dict], language: str = "en") -> InlineKeyboardMarkup:
    """
    Create keyboard for flight search results.
    
    Args:
        flights: List of flight dictionaries
        language: User's language preference
    
    Returns:
        InlineKeyboardMarkup with flight options
    """
    keyboard = []
    
    for i, flight in enumerate(flights[:10]):  # Show max 10 results
        button_text = f"✈️ {flight.get('airline', 'N/A')} - {flight.get('price', 0)} ETB"
        keyboard.append([
            InlineKeyboardButton(
                button_text,
                callback_data=f"select_flight_{i}"
            )
        ])
    
    keyboard.append([
        InlineKeyboardButton(
            "« Back",
            callback_data="back_to_menu"
        )
    ])
    
    return InlineKeyboardMarkup(keyboard)


def create_hotel_result_keyboard(hotels: List[dict], language: str = "en") -> InlineKeyboardMarkup:
    """
    Create keyboard for hotel search results.
    
    Args:
        hotels: List of hotel dictionaries
        language: User's language preference
    
    Returns:
        InlineKeyboardMarkup with hotel options
    """
    keyboard = []
    
    for i, hotel in enumerate(hotels[:10]):  # Show max 10 results
        button_text = f"🏨 {hotel.get('name', 'N/A')} - {hotel.get('price', 0)} ETB"
        keyboard.append([
            InlineKeyboardButton(
                button_text,
                callback_data=f"select_hotel_{i}"
            )
        ])
    
    keyboard.append([
        InlineKeyboardButton(
            "« Back",
            callback_data="back_to_menu"
        )
    ])
    
    return InlineKeyboardMarkup(keyboard)


def create_booking_list_keyboard(bookings: List[dict], language: str = "en") -> InlineKeyboardMarkup:
    """
    Create keyboard for booking list.
    
    Args:
        bookings: List of booking dictionaries
        language: User's language preference
    
    Returns:
        InlineKeyboardMarkup with booking options
    """
    keyboard = []
    
    for booking in bookings:
        button_text = f"{booking.get('type', 'N/A')} - {booking.get('booking_reference', 'N/A')}"
        keyboard.append([
            InlineKeyboardButton(
                button_text,
                callback_data=f"view_booking_{booking.get('booking_id')}"
            )
        ])
    
    keyboard.append([
        InlineKeyboardButton(
            "« Back",
            callback_data="back_to_menu"
        )
    ])
    
    return InlineKeyboardMarkup(keyboard)


