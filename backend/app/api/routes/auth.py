from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.security import create_access_token, decode_access_token, verify_password
from app.db.models.user import UserRecord
from app.db.session import get_db
from app.schemas.auth import TokenResponse, UserResponse

router = APIRouter(prefix="/auth", tags=["auth"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> UserRecord:
    username = decode_access_token(token)
    if not username:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = db.query(UserRecord).filter(UserRecord.username == username).first()
    if not user or not user.is_active:
        raise HTTPException(status_code=401, detail="Inactive or missing user")

    return user


@router.post("/login", response_model=TokenResponse)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
) -> TokenResponse:
    user = db.query(UserRecord).filter(UserRecord.username == form_data.username).first()

    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid username or password")

    token = create_access_token(subject=user.username)
    return TokenResponse(access_token=token)


@router.get("/me", response_model=UserResponse)
def me(current_user: UserRecord = Depends(get_current_user)) -> UserResponse:
    return UserResponse(
        id=current_user.id,
        username=current_user.username,
        is_admin=current_user.is_admin,
    )
