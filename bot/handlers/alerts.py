"""Price alerts handlers."""

import logging
from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler
from datetime import datetime, timedelta

from utils.i18n import get_text
from utils.validators import validate_number
from bot.keyboards import get_main_menu_keyboard
from models import User, PriceAlert, AlertType, AlertStatus
from config.database import SessionLocal

logger = logging.getLogger(__name__)

# Conversation states
ALERT_TYPE, TARGET_PRICE = range(2)


async def alerts_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle alerts menu callback."""
    query = update.callback_query
    await query.answer()
    
    user_id = update.effective_user.id
    
    db = SessionLocal()
    try:
        db_user = db.query(User).filter(User.user_id == user_id).first()
        language = db_user.language if db_user else "en"
        
        # Get user alerts
        alerts = db.query(PriceAlert).filter(
            PriceAlert.user_id == user_id,
            PriceAlert.status == AlertStatus.ACTIVE
        ).all()
        
        alerts_text = get_text("alerts.title", user_id=user_id, language=language) + "\n\n"
        
        if alerts:
            for alert in alerts:
                alerts_text += f"🔔 {alert.type.value} Alert\n"
                alerts_text += f"   Target: {alert.target_price:,.2f} ETB\n"
                alerts_text += f"   {get_text('alerts.status', user_id=user_id, language=language, status=alert.status.value)}\n\n"
        else:
            alerts_text += get_text("alerts.no_alerts", user_id=user_id, language=language) + "\n\n"
        
        alerts_text += get_text("alerts.create_new", user_id=user_id, language=language)
        
        keyboard = get_main_menu_keyboard(user_id=user_id, language=language)
        
        await query.edit_message_text(
            text=alerts_text,
            reply_markup=keyboard
        )
    
    finally:
        db.close()


async def create_alert_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start alert creation process."""
    user_id = update.effective_user.id
    
    db = SessionLocal()
    try:
        db_user = db.query(User).filter(User.user_id == user_id).first()
        language = db_user.language if db_user else "en"
        
        text = get_text("alerts.alert_type", user_id=user_id, language=language)
        await update.message.reply_text(text)
        
        return ALERT_TYPE
    
    finally:
        db.close()


async def alert_type_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle alert type input."""
    user_id = update.effective_user.id
    alert_type = update.message.text
    
    # Store alert type
    context.user_data['alert_type'] = alert_type
    
    db = SessionLocal()
    try:
        db_user = db.query(User).filter(User.user_id == user_id).first()
        language = db_user.language if db_user else "en"
        
        text = get_text("alerts.target_price", user_id=user_id, language=language)
        await update.message.reply_text(text)
        
        return TARGET_PRICE
    
    finally:
        db.close()


async def target_price_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle target price input and create alert."""
    user_id = update.effective_user.id
    price_str = update.message.text
    
    db = SessionLocal()
    try:
        db_user = db.query(User).filter(User.user_id == user_id).first()
        language = db_user.language if db_user else "en"
        
        is_valid, price = validate_number(price_str, min_value=1)
        
        if not is_valid:
            error_text = get_text("errors.invalid_number", user_id=user_id, language=language)
            await update.message.reply_text(error_text)
            return TARGET_PRICE
        
        # Create price alert
        alert = PriceAlert(
            user_id=user_id,
            type=AlertType.FLIGHT,  # Default to flight
            search_params=context.user_data.get('last_search', {}),
            target_price=float(price),
            currency="ETB",
            status=AlertStatus.ACTIVE,
            expires_at=datetime.now() + timedelta(days=30)
        )
        db.add(alert)
        db.commit()
        
        success_text = get_text(
            "alerts.created",
            user_id=user_id,
            language=language,
            price=f"{price:,.2f}"
        )
        keyboard = get_main_menu_keyboard(user_id=user_id, language=language)
        
        await update.message.reply_text(
            success_text,
            reply_markup=keyboard
        )
        
        logger.info(f"Created price alert for user {user_id}")
        
        return ConversationHandler.END
    
    finally:
        db.close()


async def handle_alert_deletion(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle alert deletion."""
    query = update.callback_query
    await query.answer()
    
    user_id = update.effective_user.id
    callback_data = query.data
    
    alert_id = int(callback_data.split("_")[-1])
    
    db = SessionLocal()
    try:
        db_user = db.query(User).filter(User.user_id == user_id).first()
        language = db_user.language if db_user else "en"
        
        alert = db.query(PriceAlert).filter(
            PriceAlert.alert_id == alert_id,
            PriceAlert.user_id == user_id
        ).first()
        
        if alert:
            alert.status = AlertStatus.CANCELLED
            db.commit()
            
            success_text = get_text("success.saved", user_id=user_id, language=language)
            keyboard = get_main_menu_keyboard(user_id=user_id, language=language)
            
            await query.edit_message_text(
                text=success_text,
                reply_markup=keyboard
            )
            
            logger.info(f"Deleted alert {alert_id}")
        else:
            not_found_text = get_text("errors.not_found", user_id=user_id, language=language)
            await query.edit_message_text(text=not_found_text)
    
    finally:
        db.close()


create_alert_conversation = ConversationHandler(
    entry_points=[],
    states={
        ALERT_TYPE: [lambda u, c: alert_type_input(u, c)],
        TARGET_PRICE: [lambda u, c: target_price_input(u, c)],
    },
    fallbacks=[]
)


