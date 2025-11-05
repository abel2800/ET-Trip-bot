"""Start and help command handlers."""

import logging
from telegram import Update
from telegram.ext import ContextTypes, CallbackQueryHandler

from utils.i18n import get_text, set_user_language
from bot.keyboards import get_main_menu_keyboard, get_language_keyboard
from models import User
from config.database import SessionLocal

logger = logging.getLogger(__name__)


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handle /start command.
    
    Args:
        update: Telegram update object
        context: Callback context
    """
    user = update.effective_user
    user_id = user.id
    
    # Create or get user from database
    db = SessionLocal()
    try:
        db_user = db.query(User).filter(User.user_id == user_id).first()
        
        if not db_user:
            # Create new user
            db_user = User(
                user_id=user_id,
                name=user.first_name or "User",
                language="en"
            )
            db.add(db_user)
            db.commit()
            logger.info(f"Created new user: {user_id}")
        
        # Set user language in cache
        set_user_language(user_id, db_user.language)
        
        # Send welcome message
        welcome_text = get_text("welcome", user_id=user_id)
        keyboard = get_main_menu_keyboard(user_id=user_id, language=db_user.language)
        
        await update.message.reply_text(
            welcome_text,
            reply_markup=keyboard
        )
    
    finally:
        db.close()


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handle /help command.
    
    Args:
        update: Telegram update object
        context: Callback context
    """
    user_id = update.effective_user.id
    
    db = SessionLocal()
    try:
        db_user = db.query(User).filter(User.user_id == user_id).first()
        language = db_user.language if db_user else "en"
        
        help_text = f"""
{get_text('help.title', user_id=user_id, language=language)}

{get_text('help.commands', user_id=user_id, language=language)}
/start - Start the bot
/help - Show this help message
/language - Change language
/bookings - View your bookings
/alerts - Manage price alerts

{get_text('help.contact', user_id=user_id, language=language)}
        """
        
        keyboard = get_main_menu_keyboard(user_id=user_id, language=language)
        
        await update.message.reply_text(
            help_text.strip(),
            reply_markup=keyboard
        )
    
    finally:
        db.close()


async def language_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handle language selection callback.
    
    Args:
        update: Telegram update object
        context: Callback context
    """
    query = update.callback_query
    await query.answer()
    
    user_id = update.effective_user.id
    callback_data = query.data
    
    if callback_data == "menu_language":
        # Show language selection
        text = get_text("language.title", user_id=user_id)
        keyboard = get_language_keyboard()
        
        await query.edit_message_text(
            text=text,
            reply_markup=keyboard
        )
    
    elif callback_data.startswith("lang_"):
        # Set new language
        new_language = callback_data.split("_")[1]
        
        db = SessionLocal()
        try:
            db_user = db.query(User).filter(User.user_id == user_id).first()
            
            if db_user:
                db_user.language = new_language
                db.commit()
                set_user_language(user_id, new_language)
                
                success_text = get_text("language.changed", user_id=user_id, language=new_language)
                keyboard = get_main_menu_keyboard(user_id=user_id, language=new_language)
                
                await query.edit_message_text(
                    text=success_text,
                    reply_markup=keyboard
                )
                
                logger.info(f"User {user_id} changed language to {new_language}")
        
        finally:
            db.close()


async def main_menu_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handle back to main menu callback.
    
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
        
        welcome_text = get_text("welcome", user_id=user_id, language=language)
        keyboard = get_main_menu_keyboard(user_id=user_id, language=language)
        
        await query.edit_message_text(
            text=welcome_text,
            reply_markup=keyboard
        )
    
    finally:
        db.close()


