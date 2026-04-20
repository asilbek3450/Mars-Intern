# 🚀 Deployment Checklist

## ✅ Pre-Deployment Tasks

Complete these before running the bot:

### 1. Get Bot Token from Telegram
- [ ] Open Telegram
- [ ] Search for [@BotFather](https://t.me/BotFather)
- [ ] Send `/newbot`
- [ ] Choose bot name (e.g., MarsInternBot)
- [ ] Choose bot username (e.g., @mars_intern_bot)
- [ ] Copy the token (looks like: `123456789:ABCDefGHIjklmnoPQRStuvWXYZ`)
- [ ] Save token in safe place

### 2. Create Environment File
- [ ] Navigate to project root: `cd "Mars Intern"`
- [ ] Copy template: `cp .env.example .env`
- [ ] Open `.env` with text editor
- [ ] Replace `YOUR_BOT_TOKEN_HERE` with your actual token
- [ ] Save `.env` file (DON'T commit to GitHub)
- [ ] Verify token is pasted correctly (no extra spaces)

### 3. Verify Python Installation
- [ ] Open terminal/command prompt
- [ ] Run: `python --version`
- [ ] Verify version is 3.8 or higher
- [ ] If not installed, download from [python.org](https://www.python.org)

### 4. Verify Project Files
- [ ] Check `src/main.py` exists
- [ ] Check `src/handlers.py` exists
- [ ] Check `requirements.txt` exists
- [ ] Check `run.sh` (Linux/Mac) or `run.bat` (Windows) exists
- [ ] Check `.env` file created with token

---

## 🚀 Deployment Steps

### On Linux/Mac:

```bash
# 1. Navigate to project
cd "Mars Intern"

# 2. Make script executable (one time only)
chmod +x run.sh

# 3. Run bot (auto-installs dependencies)
./run.sh
```

### On Windows:

```bash
# 1. Navigate to project
cd "Mars Intern"

# 2. Run bot (auto-installs dependencies)
run.bat
```

### Manual Setup (Any OS):

```bash
# 1. Navigate to project
cd "Mars Intern"

# 2. Create virtual environment
python -m venv venv

# 3. Activate virtual environment
# On Linux/Mac:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Run bot
cd src
python main.py
```

---

## ✅ Verification Steps

Once bot is running, perform these tests:

### 1. Check Bot Started Successfully
- [ ] Look for message: `✅ Bot started successfully!`
- [ ] Terminal shows `Waiting for messages...`
- [ ] No error messages in terminal

### 2. Test Basic Interaction
- [ ] Open Telegram
- [ ] Find your bot by username
- [ ] Send `/start` command
- [ ] Bot should respond with welcome message
- [ ] "📚 Dars kiritish" button should appear

### 3. Test Intern Selection
- [ ] Click "📚 Dars kiritish" button
- [ ] Keyboard should show list of interns (2 columns)
- [ ] Select your name from list
- [ ] Bot should send template

### 4. Test Report Submission
- [ ] Copy template from bot message
- [ ] Fill in your details (change placeholder values)
- [ ] Send filled template
- [ ] Bot should confirm receipt
- [ ] Excel file created in `data/interns_reports.xlsx`

### 5. Test Excel Storage
- [ ] Stop bot (Ctrl+C in terminal)
- [ ] Open `data/interns_reports.xlsx` with Excel/LibreOffice
- [ ] Find your name in first column
- [ ] Today's date should have your report with green highlight
- [ ] Teacher names should be listed

### 6. Test Error Handling
- [ ] Send template with wrong date format
- [ ] Bot should reject with error message
- [ ] Allow retry

### 7. Test Cancel Function
- [ ] Click "📚 Dars kiritish"
- [ ] Click "❌ Bekor qilish"
- [ ] Should return to main menu

---

## 🔍 Troubleshooting Checklist

If bot doesn't start:

### Issue: "BOT_TOKEN not set in .env file!"

**Solution**:
- [ ] Check `.env` file exists in project root
- [ ] Open `.env` and verify `BOT_TOKEN=...` is present
- [ ] Paste exact token from @BotFather (no extra spaces)
- [ ] Save file
- [ ] Restart bot

### Issue: "ModuleNotFoundError: No module named 'aiogram'"

**Solution**:
- [ ] Run: `pip install -r requirements.txt`
- [ ] Verify virtual environment is activated
- [ ] Check internet connection for downloading packages
- [ ] Try again: `pip install --upgrade aiogram`

### Issue: "Connection refused" or "Bot is not responding"

**Solution**:
- [ ] Check internet connection
- [ ] Verify token is valid (get new one from @BotFather if needed)
- [ ] Check firewall not blocking bot
- [ ] Restart bot
- [ ] Try on different network if available

### Issue: "Permission denied" on Linux/Mac

**Solution**:
```bash
chmod +x run.sh
chmod +x src/main.py
./run.sh
```

### Issue: Excel file not created

**Solution**:
- [ ] Check `data/` folder exists or can be created
- [ ] Verify write permissions: `ls -la data/`
- [ ] Try creating folder manually: `mkdir -p data`
- [ ] Check `openpyxl` installed: `pip list | grep openpyxl`
- [ ] Restart bot

### Issue: "SyntaxError" in Python files

**Solution**:
- [ ] Verify Python version is 3.8+: `python --version`
- [ ] Reinstall packages: `pip install -r requirements.txt --upgrade`
- [ ] Check for corrupted files, re-extract from source

---

## 📋 First Day Checklist

After successful deployment:

### Morning:
- [ ] Restart bot
- [ ] Verify it runs without errors
- [ ] Check it responds to `/start`

### During Day:
- [ ] Interns test submitting reports
- [ ] Monitor terminal for any errors
- [ ] Keep bot running in background window

### Evening:
- [ ] Check Excel file for all submissions
- [ ] Verify data is stored correctly
- [ ] Color coding is applied (green/red)

### Before Shutdown:
- [ ] Run: `exit` or Ctrl+C to stop bot gracefully
- [ ] Backup Excel file: `data/interns_reports.xlsx`
- [ ] Delete any test data if needed

---

## 🔄 Daily Operation

### Each Morning:
```bash
cd "Mars Intern"
./run.sh  # (or run.bat on Windows)
```

### During Day:
- Keep terminal window open
- Monitor for error messages
- Don't close terminal until end of day

### Each Evening:
```bash
# In terminal, press Ctrl+C to stop gracefully
# Or close terminal window
```

### End of Week:
- [ ] Backup `data/interns_reports.xlsx`
- [ ] Review attendance records
- [ ] Export to PDF if needed

---

## 📞 Quick Reference

### File Locations:
- Bot Code: `src/main.py`
- Interns List: `src/interns.py`
- Config: `src/config.py`
- Token: `.env` (keep secret!)
- Excel Data: `data/interns_reports.xlsx`
- Launcher: `run.sh` (Linux/Mac) or `run.bat` (Windows)

### Important Commands:
```bash
# Start bot
./run.sh  # Linux/Mac
run.bat   # Windows

# Stop bot
Ctrl+C

# Check Python version
python --version

# Install packages
pip install -r requirements.txt

# Test parser
python test_parser.py

# View Excel
open data/interns_reports.xlsx  # Mac
xdg-open data/interns_reports.xlsx  # Linux
start data/interns_reports.xlsx  # Windows
```

### Getting Help:
1. Check README.md
2. Check QUICKSTART.md
3. Check ARCHITECTURE.md
4. Check MODULE_REFERENCE.md
5. Review error message in terminal

---

## ✨ Success Indicators

Bot is working correctly when:

- ✅ Terminal shows `✅ Bot started successfully!`
- ✅ Bot responds to `/start` on Telegram
- ✅ Interns can select names
- ✅ Reports are parsed successfully
- ✅ Excel file updates automatically
- ✅ Color coding appears (green/red)
- ✅ No error messages in terminal
- ✅ Bot runs continuously without crashing

---

## 🎯 Go-Live Checklist

Before opening to all interns:

- [ ] Bot runs without errors for 30 minutes
- [ ] Test report submission works completely
- [ ] Excel file created with test data
- [ ] All 13 interns can see their names
- [ ] Error handling works (rejected bad reports)
- [ ] Backup strategy in place for Excel file
- [ ] Support person knows basic troubleshooting
- [ ] Documentation reviewed by team

**✅ READY FOR PRODUCTION**

---

## 📊 Post-Deployment Monitoring

### Daily:
- [ ] Bot still running
- [ ] No error messages
- [ ] Reports submitted and saved

### Weekly:
- [ ] Attendance data looks correct
- [ ] Excel file not corrupted
- [ ] Backup of Excel file made
- [ ] No performance issues

### Monthly:
- [ ] Review attendance trends
- [ ] Check for any missing reports
- [ ] Verify all interns using bot
- [ ] Consider any improvements

---

## 🔐 Security Reminders

- ✅ Never share `.env` file
- ✅ Never publish token in code
- ✅ Don't commit `.env` to GitHub
- ✅ Keep Excel file backups
- ✅ Verify bot token validity regularly
- ✅ Monitor for unusual activities

---

**Congratulations! Your Mars Intern Bot is ready to deploy! 🎉**

For questions, refer to the comprehensive documentation:
- DELIVERY_SUMMARY.md - Overall summary
- README.md - Full guide
- QUICKSTART.md - Fast setup
- ARCHITECTURE.md - System design
- MODULE_REFERENCE.md - Code details
