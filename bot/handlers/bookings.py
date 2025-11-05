"""My Bookings handlers."""

import logging
from telegram import Update, InputFile
from telegram.ext import ContextTypes
from io import BytesIO

from utils.i18n import get_text
from utils.pdf_generator import generate_flight_ticket, generate_hotel_confirmation
from bot.keyboards import create_booking_list_keyboard, get_main_menu_keyboard
from models import User, Booking, BookingType
from config.database import SessionLocal

logger = logging.getLogger(__name__)


async def bookings_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle bookings menu callback."""
    query = update.callback_query
    await query.answer()
    
    user_id = update.effective_user.id
    
    db = SessionLocal()
    try:
        db_user = db.query(User).filter(User.user_id == user_id).first()
        language = db_user.language if db_user else "en"
        
        # Get user bookings
        bookings = db.query(Booking).filter(Booking.user_id == user_id).order_by(Booking.created_at.desc()).all()
        
        if bookings:
            bookings_text = get_text("bookings.title", user_id=user_id, language=language) + "\n\n"
            
            for booking in bookings[:10]:  # Show latest 10
                bookings_text += f"📌 {get_text('bookings.reference', user_id=user_id, language=language, ref=booking.booking_reference)}\n"
                bookings_text += f"   {get_text('bookings.type', user_id=user_id, language=language, type=booking.type.value)}\n"
                bookings_text += f"   {get_text('bookings.status', user_id=user_id, language=language, status=booking.payment_status.value)}\n"
                bookings_text += f"   {get_text('bookings.total', user_id=user_id, language=language, price=f'{booking.total_price:,.2f}')}\n\n"
            
            keyboard = create_booking_list_keyboard(
                [b.to_dict() for b in bookings],
                language=language
            )
            
            await query.edit_message_text(
                text=bookings_text,
                reply_markup=keyboard
            )
        else:
            no_bookings_text = get_text("bookings.no_bookings", user_id=user_id, language=language)
            keyboard = get_main_menu_keyboard(user_id=user_id, language=language)
            
            await query.edit_message_text(
                text=no_bookings_text,
                reply_markup=keyboard
            )
    
    finally:
        db.close()


async def handle_booking_view(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle viewing booking details and downloading ticket."""
    query = update.callback_query
    await query.answer()
    
    user_id = update.effective_user.id
    callback_data = query.data
    
    # Extract booking ID
    booking_id = int(callback_data.split("_")[-1])
    
    db = SessionLocal()
    try:
        db_user = db.query(User).filter(User.user_id == user_id).first()
        language = db_user.language if db_user else "en"
        
        # Get booking
        booking = db.query(Booking).filter(
            Booking.booking_id == booking_id,
            Booking.user_id == user_id
        ).first()
        
        if booking:
            # Show booking details
            details_text = f"📋 {get_text('bookings.title', user_id=user_id, language=language)}\n\n"
            details_text += f"{get_text('bookings.reference', user_id=user_id, language=language, ref=booking.booking_reference)}\n"
            details_text += f"{get_text('bookings.type', user_id=user_id, language=language, type=booking.type.value)}\n"
            details_text += f"{get_text('bookings.status', user_id=user_id, language=language, status=booking.payment_status.value)}\n"
            details_text += f"{get_text('bookings.total', user_id=user_id, language=language, price=f'{booking.total_price:,.2f}')}\n"
            
            await query.edit_message_text(text=details_text)
            
            # Generate and send e-ticket/confirmation
            try:
                if booking.type == BookingType.FLIGHT:
                    pdf_buffer = generate_flight_ticket(booking.to_dict())
                    filename = f"flight_ticket_{booking.booking_reference}.pdf"
                elif booking.type == BookingType.HOTEL:
                    pdf_buffer = generate_hotel_confirmation(booking.to_dict())
                    filename = f"hotel_confirmation_{booking.booking_reference}.pdf"
                else:
                    # For tours, use flight ticket template as placeholder
                    pdf_buffer = generate_flight_ticket(booking.to_dict())
                    filename = f"booking_{booking.booking_reference}.pdf"
                
                # Send PDF
                await context.bot.send_document(
                    chat_id=user_id,
                    document=InputFile(pdf_buffer, filename=filename),
                    caption=get_text("success.ticket_sent", user_id=user_id, language=language)
                )
                
                logger.info(f"Sent e-ticket for booking {booking.booking_reference}")
            
            except Exception as e:
                logger.error(f"Error generating e-ticket: {e}")
                error_text = get_text("errors.generic", user_id=user_id, language=language)
                await context.bot.send_message(chat_id=user_id, text=error_text)
        else:
            not_found_text = get_text("errors.not_found", user_id=user_id, language=language)
            await query.edit_message_text(text=not_found_text)
    
    finally:
        db.close()


