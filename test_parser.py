"""
Demo/Test script for testing parser functionality
"""
from src.parser import ReportParser, TemplateGenerator

# Test 1: Generate template
print("=" * 60)
print("TEST 1: Template Generation")
print("=" * 60)
template = TemplateGenerator.generate_template()
print(template)
print()

# Test 2: Parse valid report
print("=" * 60)
print("TEST 2: Parse Valid Report")
print("=" * 60)
valid_report = """#hisobot
👤 Intern: Humoyun Jo'rayev
📅 Sana: 15.03.2026

🕒 ISH VAQTI:
📥 Kelgan: 09:50
📤 Ketgan: 16:20
━━━━━━━━━━━━━━━━━━

📚 DARSLAR JADVALI:

🔹 Dars #1
┣ 👨‍🏫 Ustoz: Bobur
┣ 🚪 Xona: B8-xona
┗ ⏰ Vaqt: 10:10

🔹 Dars #2
┣ 👨‍🏫 Ustoz: Sardor
┣ 🚪 Xona: A3-xona
┗ ⏰ Vaqt: 15:10"""

result = ReportParser.parse_report(valid_report)
if result:
    print("✅ Report parsed successfully!")
    print(f"   Intern: {result['intern_name']}")
    print(f"   Date: {result['date']}")
    print(f"   Arrival: {result['arrival_time']}")
    print(f"   Departure: {result['departure_time']}")
    print(f"   Lessons: {len(result['lessons'])}")
    for lesson in result['lessons']:
        print(f"      - Dars #{lesson['number']}: {lesson['teacher']}")
else:
    print("❌ Failed to parse report")
print()

# Test 3: Parse invalid report (missing teacher)
print("=" * 60)
print("TEST 3: Parse Invalid Report (Missing Teacher)")
print("=" * 60)
invalid_report_1 = """#hisobot
👤 Intern: Aziz Nosirov
📅 Sana: 15.03.2026

🕒 ISH VAQTI:
📥 Kelgan: 09:50
📤 Ketgan: 16:20
━━━━━━━━━━━━━━━━━━

📚 DARSLAR JADVALI:

🔹 Dars #1
┣ 👨‍🏫 Ustoz: 
┣ 🚪 Xona: B8-xona
┗ ⏰ Vaqt: 10:10"""

parsed_data = ReportParser.parse_report(invalid_report_1)
if not parsed_data:
    print("✅ Report validation failed as expected!")
    # Parse anyway to get error details
    import re
    lines = invalid_report_1.strip().split('\n')
    data = {
        'intern_name': None,
        'date': None,
        'arrival_time': None,
        'departure_time': None,
        'lessons': [],
    }
    intern_match = re.search(r'👤\s*Intern:\s*(.+?)(?:\n|$)', invalid_report_1)
    if intern_match:
        data['intern_name'] = intern_match.group(1).strip()
    
    date_match = re.search(r'📅\s*Sana:\s*(\d{1,2}\.\d{1,2}\.\d{4})', invalid_report_1)
    if date_match:
        date_str = date_match.group(1).strip()
        try:
            from datetime import datetime
            data['date'] = datetime.strptime(date_str, '%d.%m.%Y').date()
        except:
            pass
    
    arrival_match = re.search(r'📥\s*Kelgan:\s*(\d{1,2}:\d{2})', invalid_report_1)
    if arrival_match:
        data['arrival_time'] = arrival_match.group(1).strip()
    
    departure_match = re.search(r'📤\s*Ketgan:\s*(\d{1,2}:\d{2})', invalid_report_1)
    if departure_match:
        data['departure_time'] = departure_match.group(1).strip()
    
    error_msg = ReportParser.get_error_message(data)
    print(f"   Error: {error_msg}")
else:
    print("❌ Validation passed when it should have failed")
print()

# Test 4: Parse invalid report (bad date format)
print("=" * 60)
print("TEST 4: Parse Invalid Report (Bad Date Format)")
print("=" * 60)
invalid_report_2 = """#hisobot
👤 Intern: Baxromov Ibrohim
📅 Sana: 2026-03-15

🕒 ISH VAQTI:
📥 Kelgan: 09:50
📤 Ketgan: 16:20
━━━━━━━━━━━━━━━━━━

📚 DARSLAR JADVALI:

🔹 Dars #1
┣ 👨‍🏫 Ustoz: Bobur
┣ 🚪 Xona: B8-xona
┗ ⏰ Vaqt: 10:10"""

result = ReportParser.parse_report(invalid_report_2)
if not result:
    print("✅ Report validation failed as expected!")
    print(f"   Error: Bad date format (should be DD.MM.YYYY)")
else:
    print("❌ Validation passed when it should have failed")
print()

print("=" * 60)
print("All tests completed!")
print("=" * 60)
