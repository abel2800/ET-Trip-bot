"""Hotel search and booking handlers."""

import logging
from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler
from datetime import datetime
import uuid

from utils.i18n import get_text
from utils.validators import validate_date, validate_number
from bot.keyboards import (
    create_hotel_result_keyboard,
    get_payment_keyboard,
    get_main_menu_keyboard
)
from services import TripAPI, CurrencyConverter
from models import User, SearchHistory, Booking, SearchType, BookingType, PaymentStatus
from config.database import SessionLocal

logger = logging.getLogger(__name__)

# Conversation states
CITY, CHECKIN, CHECKOUT, ROOMS, GUESTS = range(5)

# Initialize services
trip_api = TripAPI()
currency_converter = CurrencyConverter()


async def hotels_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle hotels menu callback."""
    query = update.callback_query
    await query.answer()
    
    user_id = update.effective_user.id
    
    db = SessionLocal()
    try:
        db_user = db.query(User).filter(User.user_id == user_id).first()
        language = db_user.language if db_user else "en"
        
        text = get_text("hotels.search_title", user_id=user_id, language=language) + "\n\n"
        text += get_text("hotels.city", user_id=user_id, language=language)
        
        await query.edit_message_text(text=text)
        
        return CITY
    
    finally:
        db.close()


async def hotel_city(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle city input."""
    user_id = update.effective_user.id
    city = update.message.text
    
    context.user_data['hotel_city'] = city
    
    db = SessionLocal()
    try:
        db_user = db.query(User).filter(User.user_id == user_id).first()
        language = db_user.language if db_user else "en"
        
        text = get_text("hotels.checkin", user_id=user_id, language=language)
        await update.message.reply_text(text)
        
        return CHECKIN
    
    finally:
        db.close()


async def hotel_checkin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle check-in date input."""
    user_id = update.effective_user.id
    date_str = update.message.text
    
    db = SessionLocal()
    try:
        db_user = db.query(User).filter(User.user_id == user_id).first()
        language = db_user.language if db_user else "en"
        
        is_valid, date_obj = validate_date(date_str)
        
        if not is_valid:
            error_text = get_text("errors.invalid_date", user_id=user_id, language=language)
            await update.message.reply_text(error_text)
            return CHECKIN
        
        context.user_data['hotel_checkin'] = date_str
        
        text = get_text("hotels.checkout", user_id=user_id, language=language)
        await update.message.reply_text(text)
        
        return CHECKOUT
    
    finally:
        db.close()


async def hotel_checkout(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle check-out date input."""
    user_id = update.effective_user.id
    date_str = update.message.text
    
    db = SessionLocal()
    try:
        db_user = db.query(User).filter(User.user_id == user_id).first()
        language = db_user.language if db_user else "en"
        
        is_valid, date_obj = validate_date(date_str)
        
        if not is_valid:
            error_text = get_text("errors.invalid_date", user_id=user_id, language=language)
            await update.message.reply_text(error_text)
            return CHECKOUT
        
        context.user_data['hotel_checkout'] = date_str
        
        text = get_text("hotels.rooms", user_id=user_id, language=language)
        await update.message.reply_text(text)
        
        return ROOMS
    
    finally:
        db.close()


async def hotel_rooms(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle rooms count input."""
    user_id = update.effective_user.id
    rooms_str = update.message.text
    
    db = SessionLocal()
    try:
        db_user = db.query(User).filter(User.user_id == user_id).first()
        language = db_user.language if db_user else "en"
        
        is_valid, rooms = validate_number(rooms_str, min_value=1, max_value=10)
        
        if not is_valid:
            error_text = get_text("errors.invalid_number", user_id=user_id, language=language)
            await update.message.reply_text(error_text)
            return ROOMS
        
        context.user_data['hotel_rooms'] = rooms
        
        text = get_text("hotels.guests", user_id=user_id, language=language)
        await update.message.reply_text(text)
        
        return GUESTS
    
    finally:
        db.close()


async def hotel_guests(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle guests count input and perform search."""
    user_id = update.effective_user.id
    guests_str = update.message.text
    
    db = SessionLocal()
    try:
        db_user = db.query(User).filter(User.user_id == user_id).first()
        language = db_user.language if db_user else "en"
        
        is_valid, guests = validate_number(guests_str, min_value=1, max_value=20)
        
        if not is_valid:
            error_text = get_text("errors.invalid_number", user_id=user_id, language=language)
            await update.message.reply_text(error_text)
            return GUESTS
        
        # Perform hotel search
        searching_text = get_text("hotels.searching", user_id=user_id, language=language)
        await update.message.reply_text(searching_text)
        
        hotels = trip_api.search_hotels(
            city=context.user_data['hotel_city'],
            checkin_date=context.user_data['hotel_checkin'],
            checkout_date=context.user_data['hotel_checkout'],
            rooms=context.user_data['hotel_rooms'],
            guests=guests
        )
        
        # Convert prices to ETB
        for hotel in hotels:
            if 'price_usd' in hotel:
                hotel['price'] = currency_converter.convert_usd_to_etb(hotel['price_usd'])
        
        # Save search history
        search_history = SearchHistory(
            user_id=user_id,
            search_type=SearchType.HOTEL,
            from_city=context.user_data['hotel_city'],
            depart_date=datetime.strptime(context.user_data['hotel_checkin'], "%Y-%m-%d").date(),
            return_date=datetime.strptime(context.user_data['hotel_checkout'], "%Y-%m-%d").date(),
            rooms=context.user_data['hotel_rooms'],
            guests=guests,
            search_params=context.user_data,
            results=hotels
        )
        db.add(search_history)
        db.commit()
        
        context.user_data['hotel_results'] = hotels
        
        if hotels:
            results_text = get_text(
                "hotels.results_found",
                user_id=user_id,
                language=language,
                count=len(hotels)
            )
            keyboard = create_hotel_result_keyboard(hotels, language=language)
            
            await update.message.reply_text(
                results_text,
                reply_markup=keyboard
            )
        else:
            no_results_text = get_text("hotels.no_results", user_id=user_id, language=language)
            keyboard = get_main_menu_keyboard(user_id=user_id, language=language)
            
            await update.message.reply_text(
                no_results_text,
                reply_markup=keyboard
            )
        
        return ConversationHandler.END
    
    finally:
        db.close()


async def handle_hotel_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle hotel selection from search results."""
    query = update.callback_query
    await query.answer()
    
    user_id = update.effective_user.id
    callback_data = query.data
    
    hotel_index = int(callback_data.split("_")[-1])
    
    db = SessionLocal()
    try:
        db_user = db.query(User).filter(User.user_id == user_id).first()
        language = db_user.language if db_user else "en"
        
        hotels = context.user_data.get('hotel_results', [])
        
        if hotel_index < len(hotels):
            selected_hotel = hotels[hotel_index]
            context.user_data['selected_hotel'] = selected_hotel
            
            payment_text = get_text(
                "payment.total",
                user_id=user_id,
                language=language,
                price=f"{selected_hotel.get('price', 0):,.2f}"
            )
            payment_text += "\n\n" + get_text("payment.select_method", user_id=user_id, language=language)
            
            keyboard = get_payment_keyboard(user_id=user_id, language=language)
            
            await query.edit_message_text(
                text=payment_text,
                reply_markup=keyboard
            )
    
    finally:
        db.close()


async def handle_hotel_booking(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle hotel booking and payment."""
    query = update.callback_query
    await query.answer()
    
    user_id = update.effective_user.id
    callback_data = query.data
    
    db = SessionLocal()
    try:
        db_user = db.query(User).filter(User.user_id == user_id).first()
        language = db_user.language if db_user else "en"
        
        if callback_data == "payment_cancel":
            cancel_text = get_text("buttons.cancel", user_id=user_id, language=language)
            keyboard = get_main_menu_keyboard(user_id=user_id, language=language)
            
            await query.edit_message_text(
                text=cancel_text,
                reply_markup=keyboard
            )
            return
        
        selected_hotel = context.user_data.get('selected_hotel', {})
        payment_method = callback_data.split("_")[1]
        
        booking_reference = f"HT{uuid.uuid4().hex[:8].upper()}"
        
        booking = Booking(
            user_id=user_id,
            type=BookingType.HOTEL,
            provider=selected_hotel.get('name', 'Unknown'),
            booking_reference=booking_reference,
            booking_data=selected_hotel,
            payment_status=PaymentStatus.PENDING,
            payment_method=payment_method,
            total_price=selected_hotel.get('price', 0),
            currency="ETB"
        )
        db.add(booking)
        db.commit()
        
        processing_text = get_text("payment.processing", user_id=user_id, language=language)
        await query.edit_message_text(text=processing_text)
        
        # Simulate payment success
        booking.payment_status = PaymentStatus.COMPLETED
        db.commit()
        
        success_text = get_text(
            "success.booking_confirmed",
            user_id=user_id,
            language=language,
            ref=booking_reference
        )
        keyboard = get_main_menu_keyboard(user_id=user_id, language=language)
        
        await query.edit_message_text(
            text=success_text,
            reply_markup=keyboard
        )
        
        logger.info(f"Hotel booking created: {booking_reference}")
    
    finally:
        db.close()


hotel_search_conversation = ConversationHandler(
    entry_points=[],
    states={
        CITY: [lambda u, c: hotel_city(u, c)],
        CHECKIN: [lambda u, c: hotel_checkin(u, c)],
        CHECKOUT: [lambda u, c: hotel_checkout(u, c)],
        ROOMS: [lambda u, c: hotel_rooms(u, c)],
        GUESTS: [lambda u, c: hotel_guests(u, c)],
    },
    fallbacks=[]
)


