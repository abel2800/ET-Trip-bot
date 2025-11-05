"""Notification service for sending alerts and reminders."""

import logging
from typing import List, Dict, Any
from datetime import datetime, timedelta
from telegram import Bot

from config.settings import settings
from utils.i18n import get_text

logger = logging.getLogger(__name__)


class NotificationService:
    """Service for sending notifications to users."""
    
    def __init__(self, bot: Bot = None):
        self.bot = bot
    
    def set_bot(self, bot: Bot):
        """Set the Telegram bot instance."""
        self.bot = bot
    
    async def send_flight_reminder(
        self,
        user_id: int,
        destination: str,
        hours_before: int,
        language: str = "en"
    ):
        """
        Send flight reminder notification.
        
        Args:
            user_id: Telegram user ID
            destination: Flight destination
            hours_before: Hours before flight
            language: User's language preference
        """
        if not self.bot:
            logger.error("Bot instance not set")
            return
        
        try:
            message = get_text(
                "notifications.flight_reminder",
                user_id=user_id,
                language=language,
                destination=destination,
                hours=hours_before
            )
            
            await self.bot.send_message(
                chat_id=user_id,
                text=message
            )
            
            logger.info(f"Sent flight reminder to user {user_id}")
        
        except Exception as e:
            logger.error(f"Error sending flight reminder: {e}")
    
    async def send_hotel_reminder(
        self,
        user_id: int,
        hotel_name: str,
        language: str = "en"
    ):
        """
        Send hotel check-in reminder notification.
        
        Args:
            user_id: Telegram user ID
            hotel_name: Hotel name
            language: User's language preference
        """
        if not self.bot:
            logger.error("Bot instance not set")
            return
        
        try:
            message = get_text(
                "notifications.hotel_reminder",
                user_id=user_id,
                language=language,
                hotel=hotel_name
            )
            
            await self.bot.send_message(
                chat_id=user_id,
                text=message
            )
            
            logger.info(f"Sent hotel reminder to user {user_id}")
        
        except Exception as e:
            logger.error(f"Error sending hotel reminder: {e}")
    
    async def send_price_alert(
        self,
        user_id: int,
        item_type: str,
        new_price: float,
        language: str = "en"
    ):
        """
        Send price drop alert notification.
        
        Args:
            user_id: Telegram user ID
            item_type: Type of item (Flight/Hotel)
            new_price: New price in ETB
            language: User's language preference
        """
        if not self.bot:
            logger.error("Bot instance not set")
            return
        
        try:
            message = get_text(
                "notifications.price_drop",
                user_id=user_id,
                language=language,
                type=item_type,
                price=f"{new_price:,.2f}"
            )
            
            await self.bot.send_message(
                chat_id=user_id,
                text=message
            )
            
            logger.info(f"Sent price alert to user {user_id}")
        
        except Exception as e:
            logger.error(f"Error sending price alert: {e}")
    
    async def send_booking_confirmation(
        self,
        user_id: int,
        booking_reference: str,
        language: str = "en"
    ):
        """
        Send booking confirmation notification.
        
        Args:
            user_id: Telegram user ID
            booking_reference: Booking reference number
            language: User's language preference
        """
        if not self.bot:
            logger.error("Bot instance not set")
            return
        
        try:
            message = get_text(
                "success.booking_confirmed",
                user_id=user_id,
                language=language,
                ref=booking_reference
            )
            
            await self.bot.send_message(
                chat_id=user_id,
                text=message
            )
            
            logger.info(f"Sent booking confirmation to user {user_id}")
        
        except Exception as e:
            logger.error(f"Error sending booking confirmation: {e}")
    
    async def send_custom_message(
        self,
        user_id: int,
        message: str
    ):
        """
        Send a custom message to user.
        
        Args:
            user_id: Telegram user ID
            message: Message text
        """
        if not self.bot:
            logger.error("Bot instance not set")
            return
        
        try:
            await self.bot.send_message(
                chat_id=user_id,
                text=message
            )
            
            logger.info(f"Sent custom message to user {user_id}")
        
        except Exception as e:
            logger.error(f"Error sending custom message: {e}")


