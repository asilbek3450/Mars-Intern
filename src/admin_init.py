"""
Admin setup and initialization
"""
from database import db

# Default admin user ID - change this to your Telegram ID
DEFAULT_ADMIN_ID = 7782143104  # Set your admin user ID here


def setup_admin():
    """Initialize admin users"""
    if DEFAULT_ADMIN_ID:
        if not db.is_admin(DEFAULT_ADMIN_ID):
            db.add_admin(DEFAULT_ADMIN_ID, "Admin")
            print(f"✅ Admin qo'shildi: {DEFAULT_ADMIN_ID}")
        return True
    return False

