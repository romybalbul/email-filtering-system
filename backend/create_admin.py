from pwdlib import PasswordHash

from app.db.base import Base
from app.db.session import SessionLocal, engine
import app.db.models  # noqa: F401
from app.db.models.user import UserRecord

password_hasher = PasswordHash.recommended()

USERNAME = "admin"
PASSWORD = "ChangeMe123!"

Base.metadata.create_all(bind=engine)

db = SessionLocal()
try:
    existing = db.query(UserRecord).filter(UserRecord.username == USERNAME).first()

    if existing:
        print(f"User '{USERNAME}' already exists")
    else:
        user = UserRecord(
            username=USERNAME,
            password_hash=password_hasher.hash(PASSWORD),
            is_active=True,
            is_admin=True,
        )
        db.add(user)
        db.commit()
        print(f"Admin user '{USERNAME}' created")
        print(f"Temporary password: {PASSWORD}")
finally:
    db.close()
