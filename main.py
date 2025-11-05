"""Main entry point for Trip Ethiopia Telegram Bot."""

import logging
import asyncio
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ConversationHandler,
    filters,
)

from config.settings import settings
from config.database import init_db
from bot.handlers.start import start_command, help_command, language_callback, main_menu_callback
from bot.handlers.flights import (
    flights_menu, handle_flight_selection, handle_flight_booking,
    flight_origin, flight_destination, flight_depart_date, 
    flight_return_date, flight_passengers,
    ORIGIN, DESTINATION, DEPART_DATE, RETURN_DATE, PASSENGERS
)
from bot.handlers.hotels import (
    hotels_menu, handle_hotel_selection, handle_hotel_booking,
    hotel_city, hotel_checkin, hotel_checkout, hotel_rooms, hotel_guests,
    CITY, CHECKIN, CHECKOUT, ROOMS, GUESTS
)
from bot.handlers.tours import tours_menu, handle_tour_selection
from bot.handlers.bookings import bookings_menu, handle_booking_view
from bot.handlers.alerts import alerts_menu, handle_alert_deletion
from tasks.price_monitor import run_price_monitor_loop
from tasks.reminders import run_reminders_loop

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=getattr(logging, settings.LOG_LEVEL)
)
logger = logging.getLogger(__name__)


async def error_handler(update: Update, context):
    """Handle errors in the bot."""
    logger.error(f"Update {update} caused error {context.error}")


def main():
    """Main function to start the bot."""
    # Validate settings
    try:
        settings.validate()
    except ValueError as e:
        logger.error(f"Configuration error: {e}")
        return
    
    # Initialize database
    logger.info("Initializing database...")
    init_db()
    
    # Create bot application
    logger.info("Creating bot application...")
    application = Application.builder().token(settings.TELEGRAM_BOT_TOKEN).build()
    
    # Command handlers
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    
    # Callback query handlers
    application.add_handler(CallbackQueryHandler(language_callback, pattern="^(menu_language|lang_)"))
    application.add_handler(CallbackQueryHandler(main_menu_callback, pattern="^back_to_menu$"))
    
    # Flight conversation handler
    flight_conv_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(flights_menu, pattern="^menu_flights$")],
        states={
            ORIGIN: [MessageHandler(filters.TEXT & ~filters.COMMAND, flight_origin)],
            DESTINATION: [MessageHandler(filters.TEXT & ~filters.COMMAND, flight_destination)],
            DEPART_DATE: [MessageHandler(filters.TEXT & ~filters.COMMAND, flight_depart_date)],
            RETURN_DATE: [MessageHandler(filters.TEXT & ~filters.COMMAND, flight_return_date)],
            PASSENGERS: [MessageHandler(filters.TEXT & ~filters.COMMAND, flight_passengers)],
        },
        fallbacks=[CallbackQueryHandler(main_menu_callback, pattern="^back_to_menu$")],
    )
    application.add_handler(flight_conv_handler)
    application.add_handler(CallbackQueryHandler(handle_flight_selection, pattern="^select_flight_"))
    
    # Hotel conversation handler
    hotel_conv_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(hotels_menu, pattern="^menu_hotels$")],
        states={
            CITY: [MessageHandler(filters.TEXT & ~filters.COMMAND, hotel_city)],
            CHECKIN: [MessageHandler(filters.TEXT & ~filters.COMMAND, hotel_checkin)],
            CHECKOUT: [MessageHandler(filters.TEXT & ~filters.COMMAND, hotel_checkout)],
            ROOMS: [MessageHandler(filters.TEXT & ~filters.COMMAND, hotel_rooms)],
            GUESTS: [MessageHandler(filters.TEXT & ~filters.COMMAND, hotel_guests)],
        },
        fallbacks=[CallbackQueryHandler(main_menu_callback, pattern="^back_to_menu$")],
    )
    application.add_handler(hotel_conv_handler)
    application.add_handler(CallbackQueryHandler(handle_hotel_selection, pattern="^select_hotel_"))
    
    # Payment handlers (shared by flight and hotel)
    application.add_handler(CallbackQueryHandler(handle_flight_booking, pattern="^payment_(telebirr|cbe|cancel)$"))
    
    # Tour handlers
    application.add_handler(CallbackQueryHandler(tours_menu, pattern="^menu_tours$"))
    application.add_handler(CallbackQueryHandler(handle_tour_selection, pattern="^select_tour_"))
    
    # Bookings handlers
    application.add_handler(CallbackQueryHandler(bookings_menu, pattern="^menu_bookings$"))
    application.add_handler(CallbackQueryHandler(handle_booking_view, pattern="^view_booking_"))
    
    # Alerts handlers
    application.add_handler(CallbackQueryHandler(alerts_menu, pattern="^menu_alerts$"))
    application.add_handler(CallbackQueryHandler(handle_alert_deletion, pattern="^delete_alert_"))
    
    # Error handler
    application.add_error_handler(error_handler)
    
    # Start background tasks
    async def post_init(app):
        """Start background tasks after bot initialization."""
        logger.info("Starting background tasks...")
        bot = app.bot
        
        # Start price monitoring
        asyncio.create_task(run_price_monitor_loop(bot))
        
        # Start reminders
        asyncio.create_task(run_reminders_loop(bot))
        
        logger.info("Background tasks started")
    
    application.post_init = post_init
    
    # Start the bot
    logger.info("Starting Trip Ethiopia Bot...")
    logger.info(f"Environment: {settings.ENVIRONMENT}")
    logger.info(f"Debug mode: {settings.DEBUG}")
    
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()


