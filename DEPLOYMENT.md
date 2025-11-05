# 🚀 Deployment Guide - Trip Ethiopia Bot

This guide covers different deployment options for Trip Ethiopia Telegram Bot.

## 📋 Prerequisites

- Python 3.10+
- PostgreSQL 14+
- Redis (optional, for production)
- Telegram Bot Token from [@BotFather](https://t.me/botfather)
- Trip.com API credentials
- Payment gateway credentials (TeleBirr, CBE Birr)

## 🖥️ Local Development

### 1. Clone and Setup

```bash
# Clone repository
git clone <repository-url>
cd trip

# Run setup script
chmod +x setup.sh
./setup.sh
```

### 2. Configure Environment

Edit `.env` file with your credentials:

```env
TELEGRAM_BOT_TOKEN=your_bot_token
DATABASE_URL=postgresql://user:pass@localhost/trip_ethiopia
TRIP_COM_API_KEY=your_api_key
# ... other credentials
```

### 3. Initialize Database

```bash
# Activate virtual environment
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate  # Windows

# Run migrations
alembic upgrade head
```

### 4. Start the Bot

```bash
python main.py
```

## 🐳 Docker Deployment

### Using Docker Compose (Recommended)

```bash
# Copy environment file
cp .env.example .env
# Edit .env with your credentials

# Start all services
docker-compose up -d

# View logs
docker-compose logs -f bot

# Stop services
docker-compose down
```

### Manual Docker Build

```bash
# Build image
docker build -t trip-ethiopia-bot .

# Run container
docker run -d \
  --name trip-bot \
  --env-file .env \
  -v $(pwd)/logs:/app/logs \
  trip-ethiopia-bot
```

## ☁️ Cloud Deployment

### AWS (Amazon Web Services)

#### Using EC2

1. **Launch EC2 Instance**
   - Choose Ubuntu 22.04 LTS
   - Instance type: t3.small or larger
   - Configure security group (allow PostgreSQL, Redis ports)

2. **Connect and Setup**
   ```bash
   ssh -i your-key.pem ubuntu@your-ec2-ip
   
   # Install dependencies
   sudo apt update
   sudo apt install -y python3-pip postgresql redis-server
   
   # Clone and setup project
   git clone <repository-url>
   cd trip
   ./setup.sh
   ```

3. **Setup as Service**
   ```bash
   # Create systemd service
   sudo nano /etc/systemd/system/trip-bot.service
   ```
   
   Add:
   ```ini
   [Unit]
   Description=Trip Ethiopia Telegram Bot
   After=network.target postgresql.service
   
   [Service]
   Type=simple
   User=ubuntu
   WorkingDirectory=/home/ubuntu/trip
   Environment="PATH=/home/ubuntu/trip/venv/bin"
   ExecStart=/home/ubuntu/trip/venv/bin/python main.py
   Restart=always
   RestartSec=10
   
   [Install]
   WantedBy=multi-user.target
   ```
   
   Enable and start:
   ```bash
   sudo systemctl enable trip-bot
   sudo systemctl start trip-bot
   sudo systemctl status trip-bot
   ```

#### Using ECS (Container)

1. Build and push Docker image to ECR
2. Create ECS cluster
3. Define task definition
4. Create service
5. Configure load balancer (if using webhooks)

### DigitalOcean

#### Using Droplet

1. **Create Droplet**
   - Choose Ubuntu 22.04
   - Size: 2GB RAM or more
   - Add SSH key

2. **Setup**
   ```bash
   ssh root@your-droplet-ip
   
   # Install Docker
   curl -fsSL https://get.docker.com -o get-docker.sh
   sh get-docker.sh
   
   # Install Docker Compose
   apt install docker-compose
   
   # Clone and run
   git clone <repository-url>
   cd trip
   cp .env.example .env
   # Edit .env
   docker-compose up -d
   ```

#### Using App Platform

1. Connect your GitHub repository
2. Configure environment variables
3. Deploy

### Heroku

```bash
# Login to Heroku
heroku login

# Create app
heroku create trip-ethiopia-bot

# Add PostgreSQL
heroku addons:create heroku-postgresql:hobby-dev

# Add Redis
heroku addons:create heroku-redis:hobby-dev

# Set environment variables
heroku config:set TELEGRAM_BOT_TOKEN=your_token
heroku config:set TRIP_COM_API_KEY=your_key
# ... other variables

# Deploy
git push heroku main

# Scale worker
heroku ps:scale worker=1

# View logs
heroku logs --tail
```

Create `Procfile`:
```
worker: python main.py
```

### VPS (Generic)

Any VPS provider (Linode, Vultr, etc.):

```bash
# Install required packages
apt update
apt install -y python3-pip python3-venv postgresql redis-server git

# Clone repository
git clone <repository-url>
cd trip

# Setup
./setup.sh

# Configure database
sudo -u postgres createdb trip_ethiopia
sudo -u postgres createuser trip_user -P

# Setup systemd service (see AWS EC2 section above)
```

## 🔒 Security Considerations

### SSL/TLS

If using webhooks instead of polling:

```bash
# Get Let's Encrypt certificate
sudo apt install certbot
sudo certbot certonly --standalone -d your-domain.com
```

### Firewall

```bash
# UFW (Ubuntu)
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable
```

### Environment Variables

Never commit `.env` file! Use secrets management:

- AWS Secrets Manager
- HashiCorp Vault
- Environment variables in platform

## 📊 Monitoring

### Logging

```bash
# View logs
tail -f logs/bot.log

# With Docker
docker-compose logs -f bot
```

### Health Checks

Create a health check endpoint:

```python
# Add to main.py
from fastapi import FastAPI

app = FastAPI()

@app.get("/health")
def health_check():
    return {"status": "healthy"}
```

### Monitoring Services

- Use Sentry for error tracking
- Set up Prometheus for metrics
- Configure alerts via Telegram or email

## 🔄 Updates and Maintenance

### Manual Update

```bash
# Pull latest changes
git pull origin main

# Update dependencies
pip install -r requirements.txt

# Run migrations
alembic upgrade head

# Restart service
sudo systemctl restart trip-bot
```

### Automatic Updates (GitHub Actions)

Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Deploy to server
        uses: appleboy/ssh-action@master
        with:
          host: ${{ secrets.SERVER_HOST }}
          username: ${{ secrets.SERVER_USER }}
          key: ${{ secrets.SSH_KEY }}
          script: |
            cd /path/to/trip
            git pull
            docker-compose up -d --build
```

## 🆘 Troubleshooting

### Bot Not Responding

1. Check if bot is running: `systemctl status trip-bot`
2. Check logs: `tail -f logs/bot.log`
3. Verify bot token: `echo $TELEGRAM_BOT_TOKEN`
4. Test database connection

### Database Issues

```bash
# Check PostgreSQL status
sudo systemctl status postgresql

# Connect to database
psql -U trip_user -d trip_ethiopia

# Check tables
\dt
```

### High Memory Usage

- Increase server resources
- Optimize database queries
- Enable Redis caching
- Set up database connection pooling

## 📈 Scaling

### Horizontal Scaling

- Use multiple bot instances with webhook mode
- Load balance with nginx
- Use Redis for session storage

### Database Optimization

- Add indexes to frequently queried columns
- Use connection pooling
- Consider read replicas for search queries

## 📞 Support

For deployment issues:
- Check documentation: README.md
- Search issues on GitHub
- Contact support: support@tripethiopia.com

---

**Happy Deploying! 🚀**


