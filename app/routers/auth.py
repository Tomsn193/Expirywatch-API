
import jwt
from fastapi import APIRouter, Depends, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.limiter import limiter
from slowapi.util import get_remote_address

from app.database import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserLogin, UserResponse, Token
from app.security import (
    hash_password,
    verify_password,
    create_access_token,
    SECRET_KEY,
    ALGORITHM,
)
from app.errors import APIError as AppError


router = APIRouter(prefix="/auth", tags=["Auth"])
bearer_scheme = HTTPBearer(auto_error=False)


def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
    db: Session = Depends(get_db),
) -> User:
    if not credentials:
        raise AppError(
            401,
            "UNAUTHORIZED",
            "Missing authentication token",
        )

    try:
        payload = jwt.decode(
            credentials.credentials,
            SECRET_KEY,
            algorithms=[ALGORITHM],
        )

        user_id = payload.get("sub")

        # Validate the user ID before converting it to an integer.
        if user_id is None or not str(user_id).isdigit():
            raise AppError(
                401,
                "UNAUTHORIZED",
                "Invalid token payload",
            )

    except jwt.ExpiredSignatureError:
        raise AppError(
            401,
            "UNAUTHORIZED",
            "Token has expired",
        )
    except jwt.PyJWTError:
        raise AppError(
            401,
            "UNAUTHORIZED",
            "Invalid authentication token",
        )

    user = (
        db.query(User)
        .filter(User.id == int(user_id))
        .first()
    )

    if user is None:
        raise AppError(
            401,
            "UNAUTHORIZED",
            "User no longer exists",
        )

    return user


@router.post("/signup", response_model=UserResponse, status_code=201)
def signup(
    payload: UserCreate,
    db: Session = Depends(get_db),
):
    email = payload.email.lower()

    existing_user = (
        db.query(User)
        .filter(User.email == email)
        .first()
    )

    if existing_user is not None:
        raise AppError(
            409,
            "EMAIL_TAKEN",
            "This email is already registered",
        )

    new_user = User(
        email=email,
        password_hash=hash_password(payload.password),
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.post("/login", response_model=Token)
@limiter.limit("5/minute")
def login(
    request: Request,
    payload: UserLogin,
    db: Session = Depends(get_db),
):
    email = payload.email.lower()

    user = (
        db.query(User)
        .filter(User.email == email)
        .first()
    )

    if user is None:
        raise AppError(
            401,
            "INVALID_CREDENTIALS",
            "Incorrect email or password",
        )

    stored_hash = str(user.password_hash)

    if not verify_password(payload.password, stored_hash):
        raise AppError(
            401,
            "INVALID_CREDENTIALS",
            "Incorrect email or password",
        )

    token = create_access_token(data={"sub": str(user.id)})

    return {
        "access_token": token,
        "token_type": "bearer",
    }


@router.get("/me", response_model=UserResponse)
def get_me(
    current_user: User = Depends(get_current_user),
):
    return current_user
