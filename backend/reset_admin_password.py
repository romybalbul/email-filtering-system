from pwdlib import PasswordHash

from app.db.session import SessionLocal
from app.db.models.user import UserRecord

password_hasher = PasswordHash.recommended()

db = SessionLocal()
try:
    user = db.query(UserRecord).filter(UserRecord.username == "admin").first()
    if not user:
        print("admin user not found")
    else:
        user.password_hash = password_hasher.hash("ChangeMe123!")
        user.is_active = True
        user.is_admin = True
        db.commit()
        print("admin password reset to ChangeMe123!")
finally:
    db.close()
