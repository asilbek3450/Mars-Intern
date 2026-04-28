"""
Admin setup and initialization
"""
from database import db
from config import ADMIN_ID

def setup_admin():
    """Initialize admin users"""
    if ADMIN_ID:
        if not db.is_admin(ADMIN_ID):
            db.add_admin(ADMIN_ID, "Admin")
            print(f"✅ Admin qo'shildi: {ADMIN_ID}")
        return True
    return False
