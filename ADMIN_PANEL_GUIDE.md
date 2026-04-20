# Admin Panel Documentation

## 🔐 Admin Panel Guide

Mars Intern Bot now includes a powerful admin panel with SQLite database for complete attendance tracking and management.

---

## 📋 Table of Contents
1. [Database Setup](#database-setup)
2. [Setting Up Admin](#setting-up-admin)
3. [Admin Commands](#admin-commands)
4. [Database Structure](#database-structure)
5. [Examples](#examples)

---

## 🗄️ Database Setup

### SQLite Database
- **Location**: `data/mars_intern.db`
- **Auto-created**: Yes, on first run
- **Tables**:
  - `reports` - All attendance reports
  - `admin_users` - Admin users
  - `logs` - Activity logs

### Starting Fresh
```bash
rm data/mars_intern.db  # Delete old database
./run.sh               # Create new database
```

---

## 👤 Setting Up Admin

### Method 1: Get Your User ID First

Send any message to the bot, then:
1. Bot owner finds your Telegram ID (your_user_id)
2. Run: `/admin_add your_user_id`

### Method 2: Set in Code

Edit `admin_init.py`:
```python
DEFAULT_ADMIN_ID = 123456789  # Your Telegram ID
```

Then restart bot.

### Find Your Telegram ID
Send any message to bot and check logs:
```
User ID: 123456789
```

---

## 🎮 Admin Commands

### 1. `/admin`
Show admin menu

**Response**:
```
🔐 ADMIN PANEL

1️⃣ 📊 /stats - Bugun statistikasi
2️⃣ 📋 /reports - Bugun hisobotlari
... and more
```

### 2. `/stats`
Today's attendance statistics

**Response**:
```
📊 BUGUNGI STATISTIKA
📅 Sana: 17.04.2026

👥 Jami talabalar: 13
✅ Kelganlar: 10
❌ Kelmaganlar: 2
⏳ Hisobota kutayotganlar: 1

Kelish foizi: 76.9%
```

### 3. `/reports`
Show all today's reports

**Response**:
```
📋 BUGUNGI HISOBOTLAR (17.04.2026)

✅ Keldi Humoyun Jo'rayev
  🕒 09:50 - 16:20
  📚 2 dars: Bobur, Sardor

❌ Kelmadi Aziz Nosirov
  Sabab: Kasallik
```

### 4. `/interns_list`
Show all interns

**Response**:
```
👥 BARCHA TALABALAR

1. Ahmadjonov Salohiddin
2. Abduqaxxor Sunattilayev
... (13 total)
```

### 5. `/search_report [Talaba ismi]`
Search specific intern's reports (last 30 days)

**Example**:
```
/search_report Humoyun Jo'rayev
```

**Response**:
```
🔍 Humoyun Jo'rayev - Oxirgi 30 kun hisobotlari:

✅ 2026-04-17
   09:50 - 16:20 | 2 dars

✅ 2026-04-16
   09:45 - 16:15 | 1 dars
```

### 6. `/delete_report [Ism] [DD.MM.YYYY]`
Delete a specific report

**Example**:
```
/delete_report Humoyun\ Jo\'rayev 17.04.2026
```

**Response**:
```
✅ Hisobot o'chirildi: Humoyun Jo'rayev (17.04.2026)
```

### 7. `/admin_add [User_ID]`
Add new admin user

**Example**:
```
/admin_add 987654321
```

**Response**:
```
✅ Admin qo'shildi: 987654321
```

### 8. `/logs`
Show activity logs (last 20)

**Response**:
```
📜 FAOLIYAT JURNALI (Oxirgi 20)

👤 123456789
   ▪ report_submitted
   ▪ Intern: Humoyun Jo'rayev
   ⏰ 2026-04-17 16:20:30

👤 123456789
   ▪ stats_viewed
   ▪ Date: 2026-04-17
   ⏰ 2026-04-17 15:45:22
```

### 9. `/export_excel`
Export all data to Excel file

**Response**:
```
✅ Eksport bajarildi: reports_export_17_04_2026.xlsx
```

### 10. `/admin_help`
Show admin help and command list

---

## 🗄️ Database Structure

### Reports Table
```sql
CREATE TABLE reports (
    id INTEGER PRIMARY KEY,
    intern_name TEXT NOT NULL,
    report_date DATE NOT NULL,
    arrival_time TEXT,
    departure_time TEXT,
    lesson_count INTEGER,
    teachers TEXT,
    status TEXT ('Keldi' or 'Kelmadi'),
    absence_reason TEXT,
    created_at TIMESTAMP,
    UNIQUE(intern_name, report_date)
);
```

### Admin Users Table
```sql
CREATE TABLE admin_users (
    id INTEGER PRIMARY KEY,
    user_id INTEGER UNIQUE,
    username TEXT,
    created_at TIMESTAMP
);
```

### Logs Table
```sql
CREATE TABLE logs (
    id INTEGER PRIMARY KEY,
    user_id INTEGER,
    action TEXT,
    details TEXT,
    created_at TIMESTAMP
);
```

---

## 📊 Examples

### Get Today's Statistics
```
/stats

Output:
📊 BUGUNGI STATISTIKA
👥 Jami talabalar: 13
✅ Kelganlar: 11
❌ Kelmaganlar: 1
⏳ Hisobota kutayotganlar: 1
Kelish foizi: 84.6%
```

### Search Intern's Reports
```
/search_report Humoyun Jo'rayev

Output:
🔍 Humoyun Jo'rayev - Oxirgi 30 kun:
✅ 2026-04-17 - 09:50 - 16:20 | 2 dars
✅ 2026-04-16 - 09:45 - 16:15 | 1 dars
✅ 2026-04-15 - 10:00 - 16:30 | 3 dars
```

### Delete Mistaken Report
```
/delete_report Aziz Nosirov 17.04.2026

Output:
✅ Hisobot o'chirildi: Aziz Nosirov (17.04.2026)
```

### Add Another Admin
```
/admin_add 987654321

Output:
✅ Admin qo'shildi: 987654321
```

### View Recent Activity
```
/logs

Output:
📜 FAOLIYAT JURNALI (Oxirgi 20)

👤 123456789
   ▪ stats_viewed
   ▪ Date: 2026-04-17
   ⏰ 2026-04-17 16:20:15
```

### Export Data to Excel
```
/export_excel

Output:
✅ Eksport bajarildi: reports_export_17_04_2026.xlsx
```

---

## 🔑 Key Features

### ✅ Real-time Statistics
- View today's attendance
- See who's present and absent
- Calculate attendance percentage

### ✅ Complete History
- Search any intern's reports
- View last 30 days
- Filter by date

### ✅ Data Management
- Delete incorrect reports
- Export to Excel anytime
- Activity logging

### ✅ Admin Control
- Add multiple admins
- Track all actions
- Complete audit log

### ✅ Security
- Admin-only commands
- User ID verification
- Activity logging
- Action tracking

---

## 🛠️ Troubleshooting

### Admin Panel Not Showing
- Make sure you're an admin: `/admin_add your_id`
- Check database: `data/mars_intern.db` exists
- Restart bot: `./run.sh`

### Can't Find Your User ID
- Send any message to bot
- Check bot logs for "User ID: ..."
- Or use `/whoami` command (if available)

### Reports Not Found
- Check exact spelling of intern name
- Use exact format: `Ism Familiya`
- Date must be: `DD.MM.YYYY`

### Export Failed
- Ensure `openpyxl` installed: `pip install openpyxl`
- Check write permissions in `data/` folder
- Try again

---

## 🔐 Security Notes

1. **Admin Panel is Private**
   - Only admins can use commands
   - All actions are logged
   - User IDs are tracked

2. **Data Protection**
   - SQLite database is local
   - No data sent online
   - Backup regularly

3. **Audit Trail**
   - Every action logged
   - User ID tracked
   - Timestamp recorded

---

## 💡 Tips & Best Practices

1. **Regular Backups**
   ```bash
   cp data/mars_intern.db data/mars_intern_backup_$(date +%Y%m%d).db
   ```

2. **Weekly Reports**
   ```
   /search_report [Ism]  # Check individual
   /stats                 # Get daily summary
   /export_excel         # Export all data
   ```

3. **Monitor Attendance**
   ```
   /admin
   /stats           # Morning check
   /reports         # Evening summary
   ```

4. **Manage Mistakes**
   ```
   /delete_report [Ism] [Date]  # Fix errors
   /search_report [Ism]          # Verify
   /reports                      # Confirm
   ```

---

## 📞 Support

For issues:
1. Check command syntax
2. Verify you're an admin
3. Check database exists
4. Review logs: `/logs`
5. Restart bot and try again

---

**Admin Panel Version**: 1.0.0  
**Database**: SQLite  
**Status**: Production Ready ✅
