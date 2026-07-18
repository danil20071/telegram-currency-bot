# Telegram Currency Bot

Telegram bot for currency exchange rates with RUB/CNY focus.

## Features
- Currency converter
- Current rates
- Rate change notifications
- Target rate alerts
- Exchange offer with chat link

## Setup

### 1. Create a Telegram Bot
1. Open Telegram and search for [@BotFather](https://t.me/BotFather)
2. Send `/newbot`
3. Choose a name for your bot
4. Choose a username (must end in `bot`)
5. Save the **Bot Token** from the response

### 2. Get ExchangeRate-API Key
1. Go to [ExchangeRate-API](https://www.exchangerate-api.com/)
2. Sign up for a free account
3. Get your API key from the dashboard

### 3. Set up GitHub Secrets
1. Push the repository to GitHub
2. Go to repository **Settings > Secrets and variables > Actions**
3. Add the following secrets:
   - `TELEGRAM_BOT_TOKEN` - Your Telegram bot token
   - `EXCHANGERATE_API_KEY` - Your ExchangeRate-API key
   - `DATABASE_URL` - PostgreSQL connection string (for production)

### 4. Deploy
The bot deploys automatically via GitHub Actions when you push to `main`.

For local development:
```bash
cp .env.example .env
# Edit .env with your credentials
pip install -r requirements.txt
python main.py
```

## Commands
- `/start` - Welcome message
- `/rates` - Current rates
- `/convert [amount] [from] [to]` - Convert currency
- `/subscribe` - Subscribe to notifications
- `/target [currency] [rate]` - Set target rate
- `/exchange` - Exchange offer

## Testing
```bash
pytest tests/ -v
```
