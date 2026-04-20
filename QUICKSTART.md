# Quick Start Guide

## Prerequisites
- Python 3.8+ installed
- Telegram account
- A Telegram bot token from @BotFather

## Step 1: Get Your Bot Token

1. Open Telegram and search for [@BotFather](https://t.me/BotFather)
2. Send `/newbot` command
3. Follow the prompts and get your token
4. Copy the token (looks like: `123456789:ABCDefGHIjklmnoPQRStuvWXYZ`)

## Step 2: Setup the Project

### On Linux/Mac:
```bash
cd "Mars Intern"
cp .env.example .env
nano .env  # or edit with your editor
# Paste: BOT_TOKEN=your_token_here
chmod +x run.sh
./run.sh
```

### On Windows:
```bash
cd "Mars Intern"
copy .env.example .env
notepad .env  # Edit and paste: BOT_TOKEN=your_token_here
run.bat
```

## Step 3: Test the Bot

Once the bot is running and shows "✅ Bot started successfully!":

1. Open Telegram
2. Search for your bot (by username from step 1)
3. Send `/start`
4. Click "📚 Dars kiritish"
5. Select your name from the list
6. Fill the template and send it

## Testing Without Full Setup

To test the parser:
```bash
cd "Mars Intern"
python test_parser.py
```

## File Structure

```
Mars Intern/
├── src/                      # Main bot code
│   ├── main.py              # Entry point (run this)
│   ├── handlers.py          # Message handlers
│   ├── parser.py            # Report parsing
│   ├── excel_handler.py     # Excel storage
│   ├── config.py            # Configuration
│   ├── states.py            # FSM states
│   ├── keyboards.py         # UI components
│   ├── interns.py           # Intern list
│   └── __init__.py
├── data/                    # Auto-created for Excel file
├── requirements.txt         # Python packages
├── .env                     # Your bot token (create from .env.example)
├── run.sh / run.bat         # Launch scripts
├── test_parser.py           # Parser tests
└── README.md                # Full documentation
```

## Troubleshooting

### "❌ BOT_TOKEN not set"
- Make sure `.env` file exists in the project root
- Make sure BOT_TOKEN is set correctly (no spaces, exact token)
- Restart the bot

### "❌ Module not found"
```bash
pip install -r requirements.txt
```

### "Excel file not created"
- The `data/` folder will be created automatically
- Check file permissions if you get errors
- Try running with `python -m src.main` instead

### Bot doesn't respond
1. Check that bot is still running (check terminal)
2. Try `/start` command
3. Restart bot with Ctrl+C, then run script again

## Next Steps

1. ✅ Bot is running and tracking attendance
2. 📊 Check `data/interns_reports.xlsx` after first submission
3. 🔔 Set up daily reminders (future enhancement)
4. 📈 Generate reports (future enhancement)

## Support

For issues:
1. Check the bot is running
2. Verify token is correct
3. Check Python version: `python --version` (should be 3.8+)
4. Review logs in terminal output
