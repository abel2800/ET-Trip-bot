"""Background task for monitoring price alerts."""

import logging
import asyncio
from datetime import datetime

from models import PriceAlert, AlertType, AlertStatus, User
from services import TripAPI, CurrencyConverter, NotificationService
from config.database import SessionLocal
from config.settings import settings

logger = logging.getLogger(__name__)

trip_api = TripAPI()
currency_converter = CurrencyConverter()
notification_service = NotificationService()


async def monitor_prices():
    """Monitor active price alerts and notify users of price drops."""
    if not settings.ENABLE_PRICE_ALERTS:
        logger.info("Price alerts disabled in settings")
        return
    
    db = SessionLocal()
    try:
        # Get all active alerts
        active_alerts = db.query(PriceAlert).filter(
            PriceAlert.status == AlertStatus.ACTIVE
        ).all()
        
        logger.info(f"Monitoring {len(active_alerts)} active price alerts")
        
        for alert in active_alerts:
            try:
                # Check if alert has expired
                if alert.expires_at and alert.expires_at < datetime.now():
                    alert.status = AlertStatus.EXPIRED
                    db.commit()
                    continue
                
                # Get current price based on alert type
                current_price = None
                
                if alert.type == AlertType.FLIGHT:
                    # Search for flights with stored parameters
                    search_params = alert.search_params or {}
                    flights = trip_api.search_flights(
                        from_city=search_params.get('flight_origin', ''),
                        to_city=search_params.get('flight_destination', ''),
                        depart_date=search_params.get('flight_depart_date', ''),
                        return_date=search_params.get('flight_return_date'),
                        passengers=search_params.get('passengers', 1)
                    )
                    
                    if flights:
                        # Get lowest price
                        lowest_price_usd = min(f.get('price_usd', float('inf')) for f in flights)
                        current_price = currency_converter.convert_usd_to_etb(lowest_price_usd)
                
                elif alert.type == AlertType.HOTEL:
                    # Search for hotels with stored parameters
                    search_params = alert.search_params or {}
                    hotels = trip_api.search_hotels(
                        city=search_params.get('hotel_city', ''),
                        checkin_date=search_params.get('hotel_checkin', ''),
                        checkout_date=search_params.get('hotel_checkout', ''),
                        rooms=search_params.get('hotel_rooms', 1),
                        guests=search_params.get('guests', 1)
                    )
                    
                    if hotels:
                        # Get lowest price
                        lowest_price_usd = min(h.get('price_usd', float('inf')) for h in hotels)
                        current_price = currency_converter.convert_usd_to_etb(lowest_price_usd)
                
                # Update current price
                if current_price:
                    alert.current_price = current_price
                    db.commit()
                    
                    # Check if price is below target
                    if current_price <= alert.target_price:
                        # Get user language
                        user = db.query(User).filter(User.user_id == alert.user_id).first()
                        language = user.language if user else "en"
                        
                        # Send notification
                        await notification_service.send_price_alert(
                            user_id=alert.user_id,
                            item_type=alert.type.value,
                            new_price=current_price,
                            language=language
                        )
                        
                        # Mark alert as triggered
                        alert.status = AlertStatus.TRIGGERED
                        alert.triggered_at = datetime.now()
                        db.commit()
                        
                        logger.info(f"Triggered price alert {alert.alert_id} for user {alert.user_id}")
            
            except Exception as e:
                logger.error(f"Error monitoring alert {alert.alert_id}: {e}")
                continue
    
    except Exception as e:
        logger.error(f"Error in price monitoring task: {e}")
    
    finally:
        db.close()


async def run_price_monitor_loop(bot):
    """Run price monitoring in a loop."""
    notification_service.set_bot(bot)
    
    while True:
        try:
            await monitor_prices()
            # Wait for next check interval
            await asyncio.sleep(settings.PRICE_CHECK_INTERVAL)
        
        except Exception as e:
            logger.error(f"Error in price monitor loop: {e}")
            await asyncio.sleep(60)  # Wait 1 minute before retrying


