#!/bin/bash

# Trip Ethiopia Bot Setup Script

set -e

echo "🇪🇹 Trip Ethiopia Telegram Bot Setup"
echo "====================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.10 or higher."
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
echo "✅ Python $PYTHON_VERSION detected"
echo ""

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 is not installed. Please install pip."
    exit 1
fi

echo "✅ pip3 detected"
echo ""

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "🔌 Activating virtual environment..."
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    source venv/Scripts/activate
else
    source venv/bin/activate
fi

echo "✅ Virtual environment activated"
echo ""

# Install dependencies
echo "📥 Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo "✅ Dependencies installed"
echo ""

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "📝 Creating .env file from template..."
    cp .env.example .env
    echo "✅ .env file created"
    echo ""
    echo "⚠️  IMPORTANT: Please edit the .env file and add your API keys and tokens!"
    echo ""
else
    echo "ℹ️  .env file already exists"
    echo ""
fi

# Create necessary directories
echo "📁 Creating necessary directories..."
mkdir -p logs
mkdir -p generated_tickets
mkdir -p generated_reports
mkdir -p assets

echo "✅ Directories created"
echo ""

# Database setup
echo "🗄️  Database Setup"
echo "=================="
echo ""
read -p "Do you want to set up the database now? (y/n) " -n 1 -r
echo ""

if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "📊 Initializing database..."
    
    # Check if PostgreSQL is running
    if command -v psql &> /dev/null; then
        echo "✅ PostgreSQL detected"
        
        # Run migrations
        echo "🔄 Running database migrations..."
        alembic upgrade head
        
        echo "✅ Database initialized successfully"
    else
        echo "⚠️  PostgreSQL not detected. Please install PostgreSQL and run:"
        echo "   alembic upgrade head"
    fi
    echo ""
fi

# Summary
echo "✨ Setup Complete!"
echo "=================="
echo ""
echo "Next steps:"
echo "1. Edit the .env file and add your configuration:"
echo "   - TELEGRAM_BOT_TOKEN (from @BotFather)"
echo "   - DATABASE_URL (PostgreSQL connection string)"
echo "   - API keys for Trip.com, Currency, and Payment gateways"
echo ""
echo "2. Initialize the database (if not done already):"
echo "   alembic upgrade head"
echo ""
echo "3. Start the bot:"
echo "   python main.py"
echo ""
echo "4. Or using Docker:"
echo "   docker-compose up -d"
echo ""
echo "📚 For more information, see the README.md file"
echo ""
echo "🚀 Happy coding!"


