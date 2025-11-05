"""Tour packages handlers."""

import logging
from telegram import Update
from telegram.ext import ContextTypes

from utils.i18n import get_text
from bot.keyboards import get_main_menu_keyboard
from services import TripAPI, CurrencyConverter
from models import User
from config.database import SessionLocal

logger = logging.getLogger(__name__)

trip_api = TripAPI()
currency_converter = CurrencyConverter()


async def tours_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle tours menu callback."""
    query = update.callback_query
    await query.answer()
    
    user_id = update.effective_user.id
    
    db = SessionLocal()
    try:
        db_user = db.query(User).filter(User.user_id == user_id).first()
        language = db_user.language if db_user else "en"
        
        text = get_text("tours.title", user_id=user_id, language=language) + "\n\n"
        text += get_text("tours.searching", user_id=user_id, language=language)
        
        await query.edit_message_text(text=text)
        
        # Fetch tours
        tours = trip_api.search_tours()
        
        # Convert prices to ETB
        for tour in tours:
            if 'price_usd' in tour:
                tour['price'] = currency_converter.convert_usd_to_etb(tour['price_usd'])
        
        if tours:
            tours_text = get_text("tours.title", user_id=user_id, language=language) + "\n\n"
            
            for i, tour in enumerate(tours[:10], 1):
                tours_text += f"{i}. {tour.get('name', 'N/A')}\n"
                tours_text += f"   💰 {tour.get('price', 0):,.2f} ETB\n"
                tours_text += f"   📅 {get_text('tours.duration', user_id=user_id, language=language, days=tour.get('duration_days', 0))}\n\n"
            
            keyboard = get_main_menu_keyboard(user_id=user_id, language=language)
            
            await query.edit_message_text(
                text=tours_text,
                reply_markup=keyboard
            )
        else:
            no_results_text = get_text("tours.no_results", user_id=user_id, language=language)
            keyboard = get_main_menu_keyboard(user_id=user_id, language=language)
            
            await query.edit_message_text(
                text=no_results_text,
                reply_markup=keyboard
            )
    
    finally:
        db.close()


async def handle_tour_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle tour selection and booking."""
    query = update.callback_query
    await query.answer()
    
    user_id = update.effective_user.id
    
    db = SessionLocal()
    try:
        db_user = db.query(User).filter(User.user_id == user_id).first()
        language = db_user.language if db_user else "en"
        
        # Tour booking implementation
        text = "Tour booking coming soon!"
        keyboard = get_main_menu_keyboard(user_id=user_id, language=language)
        
        await query.edit_message_text(
            text=text,
            reply_markup=keyboard
        )
    
    finally:
        db.close()


