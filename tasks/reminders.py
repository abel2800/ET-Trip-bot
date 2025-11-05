"""Background task for sending booking reminders."""

import logging
import asyncio
from datetime import datetime, timedelta

from models import Booking, BookingType, PaymentStatus, User
from services import NotificationService
from config.database import SessionLocal
from config.settings import settings

logger = logging.getLogger(__name__)

notification_service = NotificationService()


async def send_reminders():
    """Send reminders for upcoming bookings."""
    db = SessionLocal()
    try:
        # Get all completed bookings
        bookings = db.query(Booking).filter(
            Booking.payment_status == PaymentStatus.COMPLETED
        ).all()
        
        logger.info(f"Checking {len(bookings)} bookings for reminders")
        
        for booking in bookings:
            try:
                user = db.query(User).filter(User.user_id == booking.user_id).first()
                if not user:
                    continue
                
                language = user.language
                
                if booking.type == BookingType.FLIGHT:
                    # Check flight departure time
                    booking_data = booking.booking_data or {}
                    departure_str = booking_data.get('departure_time')
                    
                    if departure_str:
                        try:
                            departure_time = datetime.fromisoformat(departure_str.replace('Z', '+00:00'))
                            hours_until_flight = (departure_time - datetime.now()).total_seconds() / 3600
                            
                            # Send reminder if flight is in 24 hours
                            if 23 <= hours_until_flight <= 25:
                                await notification_service.send_flight_reminder(
                                    user_id=booking.user_id,
                                    destination=booking_data.get('to_city', 'your destination'),
                                    hours_before=24,
                                    language=language
                                )
                                
                                logger.info(f"Sent flight reminder for booking {booking.booking_reference}")
                        
                        except (ValueError, TypeError) as e:
                            logger.error(f"Error parsing flight time: {e}")
                
                elif booking.type == BookingType.HOTEL:
                    # Check hotel check-in date
                    booking_data = booking.booking_data or {}
                    checkin_str = booking_data.get('checkin_date')
                    
                    if checkin_str:
                        try:
                            checkin_date = datetime.strptime(checkin_str, "%Y-%m-%d")
                            days_until_checkin = (checkin_date - datetime.now()).days
                            
                            # Send reminder if check-in is tomorrow
                            if days_until_checkin == 1:
                                await notification_service.send_hotel_reminder(
                                    user_id=booking.user_id,
                                    hotel_name=booking_data.get('hotel_name', 'your hotel'),
                                    language=language
                                )
                                
                                logger.info(f"Sent hotel reminder for booking {booking.booking_reference}")
                        
                        except (ValueError, TypeError) as e:
                            logger.error(f"Error parsing check-in date: {e}")
            
            except Exception as e:
                logger.error(f"Error sending reminder for booking {booking.booking_id}: {e}")
                continue
    
    except Exception as e:
        logger.error(f"Error in reminders task: {e}")
    
    finally:
        db.close()


async def run_reminders_loop(bot):
    """Run reminders in a loop."""
    notification_service.set_bot(bot)
    
    while True:
        try:
            await send_reminders()
            # Check every hour
            await asyncio.sleep(3600)
        
        except Exception as e:
            logger.error(f"Error in reminders loop: {e}")
            await asyncio.sleep(60)


