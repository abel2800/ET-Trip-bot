# 🇪🇹 Trip Ethiopia Telegram Bot

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Telegram Bot](https://img.shields.io/badge/Telegram-Bot-blue.svg)](https://core.telegram.org/bots)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A comprehensive Telegram travel assistant bot designed for Ethiopian travelers, offering flight, hotel, and tour bookings with local payment options (TeleBirr, CBE Birr).

**Live Bot:** [@ET_rip_bot](https://t.me/ET_rip_bot)

![Trip Ethiopia Bot Demo](https://img.shields.io/badge/Status-Active-success)

## 📋 Features

### Core Features
- ✈️ **Flight Search & Booking** - Search and book domestic and international flights
- 🏨 **Hotel Search & Booking** - Find and reserve hotels worldwide
- 🌍 **Tour Packages** - Browse and book Ethiopian and international tours
- 📑 **My Bookings** - Track all past and upcoming bookings
- 💰 **Price Alerts** - Set alerts for price drops on flights and hotels
- 🔔 **Notifications** - Get reminders for check-ins and upcoming trips

### Advanced Features
- 🌐 **Multi-language Support** - Amharic, Oromo, and English
- 💱 **Currency Conversion** - Real-time USD to ETB conversion
- 👥 **Group Booking Calculator** - Calculate prices for multiple travelers
- 🎁 **Referral System** - Earn rewards for inviting friends
- 🇪🇹 **Localized Experience** - Ethiopian-friendly interface and payment methods

## 🏗️ Architecture

```
[Telegram Bot] ↔ [Backend Server]
                        ↓
        ┌───────────────┼───────────────┐
        ↓               ↓               ↓
   [Trip.com API]  [Currency API]  [Payment APIs]
                        ↓
                  [PostgreSQL DB]
```

## 🚀 Installation

### Prerequisites
- Python 3.10 or higher
- PostgreSQL 14+
- Redis (for background tasks)
- Telegram Bot Token (from [@BotFather](https://t.me/botfather))

### Setup

1. **Clone the repository**
```bash
git clone <repository-url>
cd trip
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment variables**
Copy the example environment file and configure it:
```bash
cp .env.example .env
```

Then edit `.env` with your API keys:
- Get Telegram Bot Token from [@BotFather](https://t.me/botfather)
- Configure database connection
- Add Trip.com API credentials (optional for testing)
- Add payment gateway credentials (optional for testing)

**⚠️ IMPORTANT:** Never commit your `.env` file to Git!

5. **Initialize database**
```bash
alembic upgrade head
```

6. **Run the bot**
```bash
python main.py
```

## 📁 Project Structure

```
trip/
├── main.py                 # Bot entry point
├── config/
│   ├── __init__.py
│   ├── settings.py         # Configuration management
│   └── database.py         # Database connection
├── bot/
│   ├── __init__.py
│   ├── handlers/           # Command and callback handlers
│   │   ├── __init__.py
│   │   ├── start.py
│   │   ├── flights.py
│   │   ├── hotels.py
│   │   ├── tours.py
│   │   ├── bookings.py
│   │   └── alerts.py
│   ├── keyboards.py        # Inline keyboard layouts
│   └── utils.py            # Helper functions
├── services/
│   ├── __init__.py
│   ├── trip_api.py         # Trip.com API integration
│   ├── currency.py         # Currency conversion
│   ├── payment.py          # Payment processing
│   └── notifications.py    # Notification system
├── models/
│   ├── __init__.py
│   ├── user.py
│   ├── booking.py
│   ├── search.py
│   └── alert.py
├── locales/
│   ├── en.json
│   ├── am.json             # Amharic
│   └── om.json             # Oromo
├── tasks/
│   ├── __init__.py
│   ├── price_monitor.py    # Background price monitoring
│   └── reminders.py        # Booking reminders
└── utils/
    ├── __init__.py
    ├── pdf_generator.py    # E-ticket generation
    └── validators.py       # Input validation
```

## 🗄️ Database Schema

### Users Table
- `user_id` (INT, PK) - Telegram user ID
- `name` (VARCHAR)
- `language` (VARCHAR) - en, am, om
- `email` (VARCHAR, optional)
- `created_at` (TIMESTAMP)

### Bookings Table
- `booking_id` (INT, PK, auto-increment)
- `user_id` (INT, FK)
- `type` (ENUM) - Flight, Hotel, Tour
- `provider` (VARCHAR)
- `booking_data` (JSON)
- `payment_status` (ENUM) - Pending, Completed, Failed
- `total_price` (FLOAT) - in ETB
- `created_at` (TIMESTAMP)

### Search History Table
- `search_id` (INT, PK)
- `user_id` (INT, FK)
- `search_type` (ENUM) - Flight, Hotel, Tour
- `search_params` (JSON)
- `results` (JSON)
- `searched_at` (TIMESTAMP)

### Price Alerts Table
- `alert_id` (INT, PK)
- `user_id` (INT, FK)
- `type` (ENUM) - Flight, Hotel
- `search_params` (JSON)
- `target_price` (FLOAT) - in ETB
- `status` (ENUM) - Active, Triggered, Cancelled
- `created_at` (TIMESTAMP)

## 🔌 API Integrations

### Trip.com API
- Flight Search & Booking
- Hotel Search & Booking
- Tour Packages
- [Documentation](https://www.trip.com/affiliate)

### Currency API
- Real-time USD to ETB conversion
- Provider: exchangerate.host or similar

### Payment Gateways
- **TeleBirr** - Primary mobile payment
- **CBE Birr** - Bank integration
- QR code generation for manual payments

## 💳 Payment Flow

1. User selects service (flight/hotel/tour)
2. Bot calculates price in ETB
3. Bot generates payment request via TeleBirr/CBE
4. User completes payment
5. Payment gateway confirms transaction
6. Bot generates e-ticket/confirmation
7. Booking saved to database

## 🌐 Supported Languages

- **English** (en) - Default
- **Amharic** (am) - አማርኛ
- **Oromo** (om) - Afaan Oromoo

Users can switch languages anytime using `/language` command.

## 🔧 Development

### Running Tests
```bash
pytest tests/
```

### Database Migrations
```bash
# Create migration
alembic revision --autogenerate -m "description"

# Apply migration
alembic upgrade head

# Rollback
alembic downgrade -1
```

### Background Tasks
Start Celery worker for price monitoring:
```bash
celery -A tasks.celery_app worker --loglevel=info
```

## 📱 Bot Commands

- `/start` - Welcome message and main menu
- `/help` - Show help information
- `/language` - Change language preference
- `/bookings` - View my bookings
- `/alerts` - Manage price alerts
- `/cancel` - Cancel current operation

## 🚀 Deployment

### Using Docker
```bash
docker-compose up -d
```

### Manual Deployment
1. Set up PostgreSQL and Redis on server
2. Configure environment variables
3. Set up systemd service for bot
4. Configure nginx as reverse proxy (if using webhooks)
5. Set up SSL certificate

## 🔐 Security

- API keys stored in environment variables
- Database credentials encrypted
- Payment data handled securely per PCI standards
- User data protected per GDPR guidelines

## 📈 Future Enhancements

- [ ] Flight price prediction using ML
- [ ] Voice command support (Amharic/Oromo)
- [ ] Tourist guide information
- [ ] Group booking coordination
- [ ] Loyalty rewards program
- [ ] Integration with Ethiopian Airlines API

## 🤝 Contributing

Contributions are welcome! Please read CONTRIBUTING.md for details.

## 📄 License

This project is licensed under the MIT License - see LICENSE file for details.

## 📞 Support

For issues and questions:
- GitHub Issues: [Project Issues](issues-url)
- Email: support@tripethiopia.com
- Telegram: @TripEthiopiaSupport

## 👥 Team

Developed with ❤️ for Ethiopian travelers

---

**Made in Ethiopia 🇪🇹**


