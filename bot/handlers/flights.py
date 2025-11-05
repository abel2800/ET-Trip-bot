"""Flight search and booking handlers."""

import logging
from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler
from datetime import datetime

from utils.i18n import get_text
from utils.validators import validate_date, validate_number
from bot.keyboards import (
    get_ethiopian_cities_keyboard,
    get_international_cities_keyboard,
    create_flight_result_keyboard,
    get_payment_keyboard,
    get_main_menu_keyboard
)
from services import TripAPI, CurrencyConverter, PaymentProcessor
from models import User, SearchHistory, Booking, SearchType, BookingType, PaymentStatus
from config.database import SessionLocal

logger = logging.getLogger(__name__)

# Conversation states
ORIGIN, DESTINATION, DEPART_DATE, RETURN_DATE, PASSENGERS = range(5)

# Initialize services
trip_api = TripAPI()
currency_converter = CurrencyConverter()
payment_processor = PaymentProcessor()


async def flights_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handle flights menu callback.
    
    Args:
        update: Telegram update object
        context: Callback context
    """
    query = update.callback_query
    await query.answer()
    
    user_id = update.effective_user.id
    
    db = SessionLocal()
    try:
        db_user = db.query(User).filter(User.user_id == user_id).first()
        language = db_user.language if db_user else "en"
        
        text = get_text("flights.search_title", user_id=user_id, language=language) + "\n\n"
        text += get_text("flights.origin", user_id=user_id, language=language)
        
        await query.edit_message_text(text=text)
        
        # Start flight search conversation
        return ORIGIN
    
    finally:
        db.close()


async def flight_origin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle origin city input."""
    user_id = update.effective_user.id
    origin = update.message.text
    
    # Store origin in context
    context.user_data['flight_origin'] = origin
    
    db = SessionLocal()
    try:
        db_user = db.query(User).filter(User.user_id == user_id).first()
        language = db_user.language if db_user else "en"
        
        text = get_text("flights.destination", user_id=user_id, language=language)
        await update.message.reply_text(text)
        
        return DESTINATION
    
    finally:
        db.close()


async def flight_destination(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle destination city input."""
    user_id = update.effective_user.id
    destination = update.message.text
    
    # Store destination in context
    context.user_data['flight_destination'] = destination
    
    db = SessionLocal()
    try:
        db_user = db.query(User).filter(User.user_id == user_id).first()
        language = db_user.language if db_user else "en"
        
        text = get_text("flights.depart_date", user_id=user_id, language=language)
        await update.message.reply_text(text)
        
        return DEPART_DATE
    
    finally:
        db.close()


async def flight_depart_date(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle departure date input."""
    user_id = update.effective_user.id
    date_str = update.message.text
    
    db = SessionLocal()
    try:
        db_user = db.query(User).filter(User.user_id == user_id).first()
        language = db_user.language if db_user else "en"
        
        # Validate date
        is_valid, date_obj = validate_date(date_str)
        
        if not is_valid:
            error_text = get_text("errors.invalid_date", user_id=user_id, language=language)
            await update.message.reply_text(error_text)
            return DEPART_DATE
        
        # Store date in context
        context.user_data['flight_depart_date'] = date_str
        
        text = get_text("flights.return_date", user_id=user_id, language=language)
        await update.message.reply_text(text)
        
        return RETURN_DATE
    
    finally:
        db.close()


async def flight_return_date(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle return date input."""
    user_id = update.effective_user.id
    date_str = update.message.text
    
    db = SessionLocal()
    try:
        db_user = db.query(User).filter(User.user_id == user_id).first()
        language = db_user.language if db_user else "en"
        
        # Check if user wants one-way
        if date_str.lower() == 'skip':
            context.user_data['flight_return_date'] = None
        else:
            # Validate date
            is_valid, date_obj = validate_date(date_str)
            
            if not is_valid:
                error_text = get_text("errors.invalid_date", user_id=user_id, language=language)
                await update.message.reply_text(error_text)
                return RETURN_DATE
            
            context.user_data['flight_return_date'] = date_str
        
        text = get_text("flights.passengers", user_id=user_id, language=language)
        await update.message.reply_text(text)
        
        return PASSENGERS
    
    finally:
        db.close()


async def flight_passengers(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle passengers count input and perform search."""
    user_id = update.effective_user.id
    passengers_str = update.message.text
    
    db = SessionLocal()
    try:
        db_user = db.query(User).filter(User.user_id == user_id).first()
        language = db_user.language if db_user else "en"
        
        # Validate number
        is_valid, passengers = validate_number(passengers_str, min_value=1, max_value=9)
        
        if not is_valid:
            error_text = get_text("errors.invalid_number", user_id=user_id, language=language)
            await update.message.reply_text(error_text)
            return PASSENGERS
        
        # Perform flight search
        searching_text = get_text("flights.searching", user_id=user_id, language=language)
        await update.message.reply_text(searching_text)
        
        flights = trip_api.search_flights(
            from_city=context.user_data['flight_origin'],
            to_city=context.user_data['flight_destination'],
            depart_date=context.user_data['flight_depart_date'],
            return_date=context.user_data.get('flight_return_date'),
            passengers=passengers
        )
        
        # Convert prices to ETB
        for flight in flights:
            if 'price_usd' in flight:
                flight['price'] = currency_converter.convert_usd_to_etb(flight['price_usd'])
        
        # Save search history
        search_history = SearchHistory(
            user_id=user_id,
            search_type=SearchType.FLIGHT,
            from_city=context.user_data['flight_origin'],
            to_city=context.user_data['flight_destination'],
            depart_date=datetime.strptime(context.user_data['flight_depart_date'], "%Y-%m-%d").date(),
            return_date=datetime.strptime(context.user_data['flight_return_date'], "%Y-%m-%d").date() if context.user_data.get('flight_return_date') else None,
            passengers=passengers,
            search_params=context.user_data,
            results=flights
        )
        db.add(search_history)
        db.commit()
        
        # Store flights in context for later selection
        context.user_data['flight_results'] = flights
        
        if flights:
            results_text = get_text(
                "flights.results_found",
                user_id=user_id,
                language=language,
                count=len(flights)
            )
            keyboard = create_flight_result_keyboard(flights, language=language)
            
            await update.message.reply_text(
                results_text,
                reply_markup=keyboard
            )
        else:
            no_results_text = get_text("flights.no_results", user_id=user_id, language=language)
            keyboard = get_main_menu_keyboard(user_id=user_id, language=language)
            
            await update.message.reply_text(
                no_results_text,
                reply_markup=keyboard
            )
        
        return ConversationHandler.END
    
    finally:
        db.close()


async def handle_flight_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle flight selection from search results."""
    query = update.callback_query
    await query.answer()
    
    user_id = update.effective_user.id
    callback_data = query.data
    
    # Extract flight index
    flight_index = int(callback_data.split("_")[-1])
    
    db = SessionLocal()
    try:
        db_user = db.query(User).filter(User.user_id == user_id).first()
        language = db_user.language if db_user else "en"
        
        # Get selected flight from context
        flights = context.user_data.get('flight_results', [])
        
        if flight_index < len(flights):
            selected_flight = flights[flight_index]
            context.user_data['selected_flight'] = selected_flight
            
            # Show payment options
            payment_text = get_text(
                "payment.total",
                user_id=user_id,
                language=language,
                price=f"{selected_flight.get('price', 0):,.2f}"
            )
            payment_text += "\n\n" + get_text("payment.select_method", user_id=user_id, language=language)
            
            keyboard = get_payment_keyboard(user_id=user_id, language=language)
            
            await query.edit_message_text(
                text=payment_text,
                reply_markup=keyboard
            )
    
    finally:
        db.close()


async def handle_flight_booking(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle flight booking and payment."""
    query = update.callback_query
    await query.answer()
    
    user_id = update.effective_user.id
    callback_data = query.data
    
    db = SessionLocal()
    try:
        db_user = db.query(User).filter(User.user_id == user_id).first()
        language = db_user.language if db_user else "en"
        
        if callback_data == "payment_cancel":
            # Cancel booking
            cancel_text = get_text("buttons.cancel", user_id=user_id, language=language)
            keyboard = get_main_menu_keyboard(user_id=user_id, language=language)
            
            await query.edit_message_text(
                text=cancel_text,
                reply_markup=keyboard
            )
            return
        
        # Get selected flight and payment method
        selected_flight = context.user_data.get('selected_flight', {})
        payment_method = callback_data.split("_")[1]
        
        # Create booking
        import uuid
        booking_reference = f"FL{uuid.uuid4().hex[:8].upper()}"
        
        booking = Booking(
            user_id=user_id,
            type=BookingType.FLIGHT,
            provider=selected_flight.get('airline', 'Unknown'),
            booking_reference=booking_reference,
            booking_data=selected_flight,
            payment_status=PaymentStatus.PENDING,
            payment_method=payment_method,
            total_price=selected_flight.get('price', 0),
            currency="ETB"
        )
        db.add(booking)
        db.commit()
        
        # Process payment (mock for now)
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
        
        logger.info(f"Flight booking created: {booking_reference}")
    
    finally:
        db.close()


# Create conversation handler
flight_search_conversation = ConversationHandler(
    entry_points=[],
    states={
        ORIGIN: [lambda u, c: flight_origin(u, c)],
        DESTINATION: [lambda u, c: flight_destination(u, c)],
        DEPART_DATE: [lambda u, c: flight_depart_date(u, c)],
        RETURN_DATE: [lambda u, c: flight_return_date(u, c)],
        PASSENGERS: [lambda u, c: flight_passengers(u, c)],
    },
    fallbacks=[]
)


