# Architecture & Flow Documentation

## System Architecture

```
┌─────────────────────────────────────────────────────────┐
│                   TELEGRAM BOT (main.py)                 │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  ┌──────────────────────────────────────────────────┐   │
│  │     FSM State Management (states.py, config.py)  │   │
│  │                                                   │   │
│  │  • selecting_name    (Choose intern)             │   │
│  │  • waiting_for_report (Submit template)          │   │
│  │  • confirming_report  (Verify data)              │   │
│  └──────────────────────────────────────────────────┘   │
│                          ↓                               │
│  ┌──────────────────────────────────────────────────┐   │
│  │      Message Handlers (handlers.py)              │   │
│  │                                                   │   │
│  │  • cmd_start()        - Welcome                  │   │
│  │  • btn_dars_kiritish()- Show interns             │   │
│  │  • process_report()   - Parse template           │   │
│  │  • confirm_report()   - Save to Excel            │   │
│  └──────────────────────────────────────────────────┘   │
│                          ↓                               │
│  ┌──────────────────────────────────────────────────┐   │
│  │         Report Parser (parser.py)                │   │
│  │                                                   │   │
│  │  • parse_report()  - Extract data               │   │
│  │  • validate_report()- Check format              │   │
│  │  • get_error_message()- Specific errors         │   │
│  └──────────────────────────────────────────────────┘   │
│                          ↓                               │
│  ┌──────────────────────────────────────────────────┐   │
│  │      Excel Handler (excel_handler.py)            │   │
│  │                                                   │   │
│  │  • add_record()     - Save to Excel             │   │
│  │  • apply_formatting()- Color coding             │   │
│  │  • check_attendance()- Query absences           │   │
│  └──────────────────────────────────────────────────┘   │
│                          ↓                               │
│  ┌──────────────────────────────────────────────────┐   │
│  │      Data Storage (interns_reports.xlsx)         │   │
│  │                                                   │   │
│  │  [Keldi] = Green highlighting                   │   │
│  │  [Kelmadi] = Red highlighting                   │   │
│  └──────────────────────────────────────────────────┘   │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

## User Flow Diagram

```
                          START
                            ↓
                    User sends /start
                            ↓
                ┌───────────────────────┐
                │  Show Main Menu       │
                │  📚 Dars kiritish     │
                └───────────────────────┘
                            ↓
                User clicks "📚 Dars kiritish"
                            ↓
                ┌───────────────────────┐
                │  selecting_name (FSM) │
                │  Show 13 interns      │
                │  in 2-column layout   │
                └───────────────────────┘
                            ↓
                User selects their name
                            ↓
                ┌───────────────────────┐
                │  waiting_for_report   │
                │  Send template:       │
                │  #hisobot             │
                │  👤 Intern: [Name]    │
                │  📅 Sana: DD.MM.YYYY  │
                │  🕒 ISH VAQTI:        │
                │  📚 DARSLAR JADVALI:  │
                └───────────────────────┘
                            ↓
                User fills & sends template
                            ↓
                ┌────────────────────────┐
                │  Parser (parse.py)     │
                │  Extract:              │
                │  • Name                │
                │  • Date                │
                │  • Times               │
                │  • Lessons & Teachers  │
                └────────────────────────┘
                            ↓
                    ┌─────────────────┐
                    │  Validation     │
                    │    Check All    │
                    │    Fields ✓     │
                    └─────────────────┘
                     ↙                  ↖
              Valid Data          Invalid
                   ↓                   ↓
        ┌──────────────────┐  ┌──────────────────┐
        │ confirming_report│  │ Error Message    │
        │ Show Summary:    │  │ Retry? ← Yes     │
        │ ✅ Ha / ❌ Yo'q  │  │         ↓         │
        └──────────────────┘  │ waiting_for_report
             ↙        ↖       │ (retry loop)     │
           Yes        No      └──────────────────┘
             ↓         ↓
        ┌─────────────────┐
        │ Excel Handler   │  ← No
        │ Save Record:    │
        │ • Name (🟢/🔴)  │  → wait_for_report
        │ • Date Column   │
        │ • Lessons Count │
        │ • Teachers      │
        └─────────────────┘
             ↓
    ✅ Success Message
        "Rahmat!"
             ↓
    ┌───────────────────────┐
    │  Back to Main Menu    │
    │  📚 Dars kiritish     │
    └───────────────────────┘
```

## Data Flow Diagram

```
User Message (Raw Text)
         ↓
┌────────────────────────────────┐
│   Message Handler              │
│   (handlers.py)                │
│ • Receive message              │
│ • Check format (#hisobot)      │
└────────────────────────────────┘
         ↓
┌────────────────────────────────┐
│   Report Parser                │
│   (parser.py)                  │
│ • Extract with regex           │
│ • Match emojis & fields        │
│ • Create structured dict       │
└────────────────────────────────┘
         ↓
    Parsed Dict:
    {
      'intern_name': 'Humoyun Jo\'rayev',
      'date': date(2026, 3, 15),
      'arrival_time': '09:50',
      'departure_time': '16:20',
      'lessons': [
        {
          'number': '1',
          'teacher': 'Bobur',
          'room': 'B8-xona',
          'time': '10:10'
        },
        ...
      ],
      'status': 'Keldi',
      'raw_text': '...'
    }
         ↓
┌────────────────────────────────┐
│   Validation                   │
│ • Required fields present?     │
│ • Correct formats?             │
│ • At least 1 lesson?           │
│ • Valid times?                 │
└────────────────────────────────┘
         ↓
    Valid ✓ / Invalid ✗
         ↓
┌────────────────────────────────┐
│   Excel Handler                │
│   (excel_handler.py)           │
│ • Connect to file              │
│ • Find intern row              │
│ • Add/create date column       │
│ • Format cells (colors)        │
│ • Save to disk                 │
└────────────────────────────────┘
         ↓
    Excel File Created/Updated:
    
    | Ism Familiya | 15.03.2026 |
    |---|---|
    | Humoyun | [Keldi] 2 dars |
    |         | Bobur, Sardor  | (🟢 Green)
```

## Module Interaction

```
main.py
  ├─→ config.py (Load settings)
  ├─→ handlers.py (Register handlers)
  │    ├─→ parser.py (Parse reports)
  │    │    └─→ interns.py (Validate names)
  │    ├─→ excel_handler.py (Save data)
  │    │    └─→ interns.py (Full list)
  │    ├─→ keyboards.py (UI components)
  │    └─→ states.py (FSM states)
  └─→ asyncio (Event loop)
```

## FSM State Machine

```
                    ┌─────────────────────┐
                    │   selecting_name    │
                    │ (Choose intern name)│
                    └─────────────────────┘
                     ↙ User selects ↖
                     ↓            ↓
            ┌─────────────────┐  (Cancel)
            │waiting_for_report
            │ (Submit template) ←─→ Retry on error
            └─────────────────┘
                     ↓
            ┌──────────────────┐
            │ confirming_report│
            │ (Verify data)    │
            └──────────────────┘
              ↙          ↖
            (Ha)        (Yo'q)
             ↓            ↓
           Save       Return to
           (Done)     waiting_for_report


At any state: /start → Reset to initial state
At any state: Cancel button → Return to Main Menu
```

## Excel File Structure

```
┌──────────────────────────────────────────────────────────────┐
│                    HEADER ROW (Styled)                        │
├──────────────────────────────────────────────────────────────┤
│ Ism Familiya │ 15.03.2026 │ 16.03.2026 │ 17.03.2026 │        │
├──────────────────────────────────────────────────────────────┤
│Humoyun Jo'ray│[Keldi]     │[Kelmadi]   │[Keldi]     │        │
│              │2 dars      │Kasallik    │3 dars      │        │
│              │Bobur,Sardor│            │Teacher1,T2,│🟢 Green│
│              │            │            │Teacher3    │        │
├──────────────────────────────────────────────────────────────┤
│Aziz Nosirov  │[Kelmadi]   │[Keldi]     │[Keldi]     │        │
│              │Shaxsiy ishlar│ 1 dars   │ 2 dars     │        │
│              │            │Teacher1    │Teacher1,T2 │🔴 Red  │
│              │            │            │            │🟢 Green│
├──────────────────────────────────────────────────────────────┤
│... 11 more ..│            │            │            │        │
│   interns    │            │            │            │        │
└──────────────────────────────────────────────────────────────┘

Legend:
🟢 Green = [Keldi] - Attended (marked automatically)
🔴 Red   = [Kelmadi] - Absent (marked automatically)
- Rows auto-height to 40pt for readability
- Name column width: 25
- Date columns width: 30
```

## Error Handling Flow

```
Report Submission
        ↓
    ┌───────────────┐
    │ Parse Report  │
    └───────────────┘
        ↓
    ┌──────────────────────────────┐
    │ Check Each Validation        │
    │ 1. Intern name?              │──→ Error: "Ism yo'q"
    │ 2. Date format? (DD.MM.YYYY) │──→ Error: "Sana noto'g'ri"
    │ 3. Time format? (HH:MM)      │──→ Error: "Vaqt noto'g'ri"
    │ 4. Lessons exist?            │──→ Error: "Darslar bo'sh"
    │ 5. Teacher names?            │──→ Error: "Ustoz nomi"
    │ 6. Lesson times?             │──→ Error: "Dars vaqti"
    └──────────────────────────────┘
        ↓
    All Valid?
    ↙        ↖
   Yes        No
    ↓         ↓
  Save    Show Error
  Success + Retry Option

User can keep trying until correct!
```

## Regex Patterns Used

```
Intern Name:    r'👤\s*Intern:\s*(.+?)(?:\n|$)'
Date:           r'📅\s*Sana:\s*(\d{1,2}\.\d{1,2}\.\d{4})'
Arrival Time:   r'📥\s*Kelgan:\s*(\d{1,2}:\d{2})'
Departure Time: r'📤\s*Ketgan:\s*(\d{1,2}:\d{2})'
Lesson Block:   r'🔹\s*Dars\s*#(\d+)(.*?)(?=🔹|$)'
Teacher:        r'Ustoz:\s*([^\n┣]*)'
Room:           r'Xona:\s*([^\n┣]*)'
Lesson Time:    r'Vaqt:\s*(\d{1,2}:\d{2})'

Note: Uses [^\n┣]* instead of [^\n]* to handle emoji chars
```

## Database Schema (Excel)

```
CREATE COLUMNS:
- Ism Familiya (Primary - all 13 interns)
- DD.MM.YYYY (Dynamic - created for each date)

CELL VALUE FORMAT:
For Keldi (Present):
  [Keldi] {lesson_count} dars
  {teacher1}, {teacher2}, ...

For Kelmadi (Absent):
  [Kelmadi] {reason}

STYLING:
- Green for [Keldi] entries
- Red for [Kelmadi] entries
- Text wrapping enabled
- Row height: 40pt
```

## Dependencies Graph

```
aiogram 3.3.0
  ├─ aiohttp (async HTTP)
  ├─ magic-filter
  └─ multidict

pandas 2.1.4
  ├─ numpy
  └─ python-dateutil

openpyxl 3.1.2
  ├─ et_xmlfile
  └─ packaging

python-dotenv 1.0.0
  └─ (no dependencies)

aiofiles 23.2.1
  └─ (no dependencies)
```

---

**This document provides a complete architectural overview of the Mars Intern Telegram Bot system.**
