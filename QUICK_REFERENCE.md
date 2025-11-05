# 📖 Quick Reference Guide - Trip Ethiopia Bot

## 🚀 Quick Commands

### Running the Bot
```bash
# Local development
python main.py

# With Docker
docker-compose up -d

# View logs
tail -f logs/bot.log
docker-compose logs -f bot
```

### Database Operations
```bash
# Create migration
alembic revision --autogenerate -m "description"

# Apply migrations
alembic upgrade head

# Rollback one migration
alembic downgrade -1

# View current version
alembic current

# View migration history
alembic history
```

### Testing
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=. --cov-report=html

# Run specific test
pytest tests/test_basic.py -v

# Run marked tests
pytest -m unit
```

### Docker Commands
```bash
# Build image
docker build -t trip-ethiopia-bot .

# Start services
docker-compose up -d

# Stop services
docker-compose down

# Restart specific service
docker-compose restart bot

# View logs
docker-compose logs -f bot

# Execute command in container
docker-compose exec bot python -c "print('Hello')"

# Shell access
docker-compose exec bot /bin/bash
```

## 📁 Project Structure Reference

```
trip/
├── main.py                      # Bot entry point
│
├── config/                      # Configuration
│   ├── settings.py             # App settings
│   └── database.py             # DB configuration
│
├── bot/                         # Bot logic
│   ├── handlers/               # Command handlers
│   │   ├── start.py           # /start, /help, language
│   │   ├── flights.py         # Flight search/booking
│   │   ├── hotels.py          # Hotel search/booking
│   │   ├── tours.py           # Tour packages
│   │   ├── bookings.py        # My bookings
│   │   └── alerts.py          # Price alerts
│   ├── keyboards.py            # Keyboard layouts
│   └── utils.py                # Helper functions
│
├── models/                      # Database models
│   ├── user.py                 # User model
│   ├── booking.py              # Booking model
│   ├── search.py               # Search history
│   └── alert.py                # Price alerts
│
├── services/                    # External integrations
│   ├── trip_api.py             # Trip.com API
│   ├── currency.py             # Currency conversion
│   ├── payment.py              # Payment processing
│   └── notifications.py        # Notifications
│
├── tasks/                       # Background tasks
│   ├── price_monitor.py        # Price monitoring
│   └── reminders.py            # Booking reminders
│
├── utils/                       # Utilities
│   ├── i18n.py                 # Internationalization
│   ├── validators.py           # Input validation
│   └── pdf_generator.py        # PDF/ticket generation
│
├── locales/                     # Translations
│   ├── en.json                 # English
│   ├── am.json                 # Amharic
│   └── om.json                 # Oromo
│
├── alembic/                     # Database migrations
└── tests/                       # Test files
```

## 🎯 Common Tasks

### Adding a New Feature

1. **Create handler** in `bot/handlers/feature.py`
2. **Add keyboard** in `bot/keyboards.py` if needed
3. **Add translations** in `locales/*.json`
4. **Register handler** in `main.py`
5. **Add tests** in `tests/test_feature.py`

### Adding a New Language

1. Create `locales/xx.json` (copy from `en.json`)
2. Translate all strings
3. Add language code to `settings.py` SUPPORTED_LANGUAGES
4. Test with `/language` command

### Creating Database Model

1. Create model in `models/`
2. Import in `models/__init__.py`
3. Import in `alembic/env.py`
4. Generate migration: `alembic revision --autogenerate -m "add table"`
5. Apply: `alembic upgrade head`

### Adding API Integration

1. Create service in `services/api_name.py`
2. Add credentials to `.env`
3. Add settings to `config/settings.py`
4. Import in `services/__init__.py`
5. Use in handlers

## 💡 Code Snippets

### Getting User Language
```python
from models import User
from config.database import SessionLocal

db = SessionLocal()
user = db.query(User).filter(User.user_id == user_id).first()
language = user.language if user else "en"
db.close()
```

### Sending Translated Message
```python
from utils.i18n import get_text

text = get_text("key.path", user_id=user_id, param=value)
await update.message.reply_text(text)
```

### Creating Keyboard
```python
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

keyboard = [
    [InlineKeyboardButton("Text", callback_data="action")],
]
reply_markup = InlineKeyboardMarkup(keyboard)
```

### Database Query
```python
from models import Booking
from config.database import SessionLocal

db = SessionLocal()
try:
    bookings = db.query(Booking).filter(
        Booking.user_id == user_id
    ).order_by(Booking.created_at.desc()).all()
finally:
    db.close()
```

### Currency Conversion
```python
from services import CurrencyConverter

converter = CurrencyConverter()
etb_price = converter.convert_usd_to_etb(usd_price)
```

## 🔧 Environment Variables

### Required
```env
TELEGRAM_BOT_TOKEN=your_bot_token
DATABASE_URL=postgresql://user:pass@host/db
```

### Optional (Development)
```env
ENVIRONMENT=development
DEBUG=True
LOG_LEVEL=INFO
```

### Optional (Production)
```env
TRIP_COM_API_KEY=your_key
TRIP_COM_API_SECRET=your_secret
TELEBIRR_API_KEY=your_key
CBE_BIRR_API_KEY=your_key
REDIS_URL=redis://localhost:6379/0
```

## 📊 Database Schema Quick Reference

### Users Table
- `user_id` (BigInt, PK) - Telegram user ID
- `name` (String) - User name
- `language` (String) - Language preference
- `email` (String) - Email (optional)

### Bookings Table
- `booking_id` (Int, PK) - Auto-increment
- `user_id` (BigInt, FK) - User reference
- `type` (Enum) - Flight/Hotel/Tour
- `booking_reference` (String) - Unique reference
- `total_price` (Float) - Price in ETB
- `payment_status` (Enum) - Pending/Completed/Failed

### Search History Table
- `search_id` (Int, PK) - Auto-increment
- `user_id` (BigInt, FK) - User reference
- `search_type` (Enum) - Flight/Hotel/Tour
- `search_params` (JSON) - Search parameters
- `results` (JSON) - Search results

### Price Alerts Table
- `alert_id` (Int, PK) - Auto-increment
- `user_id` (BigInt, FK) - User reference
- `type` (Enum) - Flight/Hotel
- `target_price` (Float) - Target price in ETB
- `status` (Enum) - Active/Triggered/Cancelled

## 🎨 Bot Commands

User commands:
- `/start` - Start bot and show main menu
- `/help` - Show help information
- `/language` - Change language preference

Admin commands (for future):
- `/stats` - Show bot statistics
- `/broadcast` - Send message to all users
- `/backup` - Backup database

## 🔐 Security Checklist

- [ ] Environment variables in `.env` (not committed)
- [ ] Strong database password
- [ ] Bot token kept secret
- [ ] API keys encrypted
- [ ] Input validation on all user inputs
- [ ] SQL injection prevention (using ORM)
- [ ] Rate limiting configured
- [ ] HTTPS for webhooks (production)

## 📈 Performance Tips

1. **Database:**
   - Add indexes on frequently queried columns
   - Use connection pooling
   - Clean old search history periodically

2. **Bot:**
   - Use Redis for caching
   - Batch database operations
   - Optimize message sending

3. **API Calls:**
   - Cache currency rates
   - Implement retry logic
   - Use async operations

## 🆘 Troubleshooting Quick Fixes

### Bot not responding
```bash
sudo systemctl restart trip-bot
```

### Database connection error
```bash
sudo systemctl status postgresql
psql -U trip_user -d trip_ethiopia
```

### Clear Python cache
```bash
find . -type d -name __pycache__ -exec rm -rf {} +
find . -type f -name "*.pyc" -delete
```

### Rebuild Docker
```bash
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

## 📞 Support

- Documentation: `README.md`, `GETTING_STARTED.md`
- Deployment: `DEPLOYMENT.md`
- Contributing: `CONTRIBUTING.md`
- Issues: GitHub Issues
- Email: support@tripethiopia.com

---

**Quick reference for Trip Ethiopia Bot developers**


