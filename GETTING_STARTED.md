# 🚀 Getting Started with Trip Ethiopia Bot

Welcome! This guide will help you set up and run the Trip Ethiopia Telegram Bot quickly.

## 📋 Quick Start Checklist

- [ ] Python 3.10+ installed
- [ ] PostgreSQL installed
- [ ] Telegram account
- [ ] Bot token from @BotFather
- [ ] Trip.com API credentials (optional for testing)

## 🔑 Step 1: Create Your Telegram Bot

1. Open Telegram and search for [@BotFather](https://t.me/botfather)
2. Send `/newbot` command
3. Choose a name: `Trip Ethiopia Bot`
4. Choose a username: `trip_ethiopia_bot` (must be unique)
5. Copy the bot token (looks like: `123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11`)

## 💻 Step 2: Install Requirements

### On Ubuntu/Debian

```bash
# Update system
sudo apt update

# Install Python and PostgreSQL
sudo apt install -y python3 python3-pip python3-venv postgresql postgresql-contrib

# Start PostgreSQL
sudo systemctl start postgresql
sudo systemctl enable postgresql
```

### On macOS

```bash
# Install Homebrew (if not installed)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Python and PostgreSQL
brew install python@3.11 postgresql

# Start PostgreSQL
brew services start postgresql
```

### On Windows

1. Download and install [Python 3.11](https://www.python.org/downloads/)
2. Download and install [PostgreSQL](https://www.postgresql.org/download/windows/)
3. Add Python and PostgreSQL to PATH

## 📥 Step 3: Download and Setup Project

```bash
# Clone or download the project
cd /path/to/your/projects

# Navigate to project
cd trip

# Run setup script
chmod +x setup.sh  # On Linux/Mac
./setup.sh

# On Windows, run manually:
# python -m venv venv
# venv\Scripts\activate
# pip install -r requirements.txt
```

## 🗄️ Step 4: Setup Database

### Create Database

```bash
# On Linux/Mac
sudo -u postgres psql
```

```sql
-- In PostgreSQL shell
CREATE DATABASE trip_ethiopia;
CREATE USER trip_user WITH PASSWORD 'your_secure_password';
GRANT ALL PRIVILEGES ON DATABASE trip_ethiopia TO trip_user;
\q
```

### Configure Database Connection

Edit `.env` file:

```env
DATABASE_URL=postgresql://trip_user:your_secure_password@localhost:5432/trip_ethiopia
```

### Run Migrations

```bash
# Activate virtual environment
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate  # Windows

# Run migrations
alembic upgrade head
```

## ⚙️ Step 5: Configure Bot

Edit `.env` file and add your credentials:

```env
# Required
TELEGRAM_BOT_TOKEN=your_bot_token_from_botfather
DATABASE_URL=postgresql://trip_user:password@localhost:5432/trip_ethiopia

# Optional (for testing, use mock mode)
TRIP_COM_API_KEY=your_trip_com_key
TRIP_COM_API_SECRET=your_trip_com_secret

# Optional (for testing, use mock payments)
TELEBIRR_API_KEY=test_key
TELEBIRR_API_SECRET=test_secret
CBE_BIRR_API_KEY=test_key
CBE_BIRR_API_SECRET=test_secret

# App Settings
ENVIRONMENT=development
DEBUG=True
LOG_LEVEL=INFO
```

## 🎯 Step 6: Run the Bot

```bash
# Make sure virtual environment is activated
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate  # Windows

# Start the bot
python main.py
```

You should see:

```
INFO - Starting Trip Ethiopia Bot...
INFO - Environment: development
INFO - Debug mode: True
INFO - Bot polling started
```

## 📱 Step 7: Test Your Bot

1. Open Telegram
2. Search for your bot username
3. Send `/start` command
4. You should see the welcome message with menu options

### Test Features

Try these commands:
- `/start` - Welcome message
- `/help` - Help information
- Choose "✈️ Flights" - Test flight search
- Choose "🌐 Language" - Change language

## 🧪 Test Mode

The bot works in test mode without actual API credentials:

- **Flight/Hotel searches** return mock data
- **Payments** are simulated (no actual charges)
- **All features** work for demonstration

## 🎨 Customization

### Change Bot Name and Description

1. Go to @BotFather
2. Send `/mybots`
3. Select your bot
4. Choose "Edit Bot" > "Edit Description"

### Add Bot Profile Picture

1. Go to @BotFather
2. Select your bot
3. Choose "Edit Bot" > "Edit Botpic"
4. Upload your image

### Set Bot Commands

```
start - Start the bot
help - Get help and support
language - Change language
bookings - View my bookings
alerts - Manage price alerts
```

## 🔧 Troubleshooting

### Bot Doesn't Respond

**Check if bot is running:**
```bash
ps aux | grep main.py
```

**Check logs:**
```bash
tail -f logs/bot.log
```

**Verify bot token:**
```bash
echo $TELEGRAM_BOT_TOKEN
```

### Database Connection Error

**Check PostgreSQL status:**
```bash
sudo systemctl status postgresql
```

**Test connection:**
```bash
psql -U trip_user -d trip_ethiopia
```

### Import Errors

**Reinstall dependencies:**
```bash
pip install --upgrade -r requirements.txt
```

### Port Already in Use

If running multiple instances:
```bash
# Find process
lsof -i :8443

# Kill process
kill -9 <PID>
```

## 🐳 Using Docker (Alternative)

If you prefer Docker:

```bash
# Copy environment file
cp .env.example .env
# Edit .env with your credentials

# Start with Docker Compose
docker-compose up -d

# View logs
docker-compose logs -f bot

# Stop
docker-compose down
```

## 📚 Next Steps

1. **Read the full documentation:** `README.md`
2. **Configure real APIs:** Get Trip.com credentials
3. **Set up payment gateways:** Configure TeleBirr/CBE Birr
4. **Deploy to production:** See `DEPLOYMENT.md`
5. **Contribute:** See `CONTRIBUTING.md`

## 🆘 Getting Help

### Common Issues

**Problem:** Bot token invalid
- **Solution:** Double-check token from @BotFather, no extra spaces

**Problem:** Database connection refused
- **Solution:** Ensure PostgreSQL is running and credentials are correct

**Problem:** Module not found errors
- **Solution:** Activate virtual environment and reinstall requirements

### Support Channels

- **Documentation:** Check README.md and other .md files
- **Issues:** Create an issue on GitHub
- **Email:** support@tripethiopia.com

## 📖 Learning Resources

### Python & Telegram Bots
- [python-telegram-bot documentation](https://docs.python-telegram-bot.org/)
- [Telegram Bot API](https://core.telegram.org/bots/api)

### PostgreSQL
- [PostgreSQL Tutorial](https://www.postgresqltutorial.com/)

### Python Async
- [Python asyncio documentation](https://docs.python.org/3/library/asyncio.html)

## ✅ Verification Checklist

Before you start developing:

- [ ] Bot responds to `/start` command
- [ ] Main menu buttons work
- [ ] Language switching works
- [ ] Can navigate through menus
- [ ] Database is created and accessible
- [ ] Logs are being written to `logs/` directory

## 🎉 Success!

If everything works, congratulations! You now have a fully functional travel booking bot.

### What You Can Do Now

1. **Customize** the bot for your needs
2. **Add more features** (see CONTRIBUTING.md)
3. **Deploy to production** (see DEPLOYMENT.md)
4. **Share** with Ethiopian travelers

---

**Welcome to Trip Ethiopia Bot! 🇪🇹✈️**

*Making Ethiopian travel easier, one booking at a time.*


