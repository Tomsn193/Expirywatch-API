import jwt
from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse, Token
from app.security import hash_password, verify_password, create_access_token, SECRET_KEY, ALGORITHM
from app.errors import APIError as AppError  # Aliased to match your APIError class

router = APIRouter(prefix="/auth", tags=["Auth"])
bearer_scheme = HTTPBearer(auto_error=False)


def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
    db: Session = Depends(get_db),
) -> User:
    if not credentials:
        raise AppError(401, "UNAUTHORIZED", "Missing authentication token")

    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")  # Removed strict : str annotation to satisfy linter
        if user_id is None:
            raise AppError(401, "UNAUTHORIZED", "Invalid token payload")
    except jwt.ExpiredSignatureError:
        raise AppError(401, "UNAUTHORIZED", "Token has expired")
    except jwt.PyJWTError:
        raise AppError(401, "UNAUTHORIZED", "Invalid authentication token")

    user = db.query(User).filter(User.id == int(user_id)).first()
    if not user:
        raise AppError(401, "UNAUTHORIZED", "User no longer exists")

    return user


@router.post("/signup", response_model=UserResponse, status_code=201)
def signup(payload: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == payload.email).first()
    if existing_user:
        raise AppError(409, "EMAIL_TAKEN", "This email is already registered")

    new_user = User(
        email=payload.email.lower(),
        password_hash=hash_password(payload.password),
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.post("/login", response_model=Token)
def login(payload: UserCreate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == payload.email.lower()).first()

    # Split checks so the linter confirms 'user' is not None before verifying password
    if not user:
        raise AppError(401, "INVALID_CREDENTIALS", "Incorrect email or password")

    stored_hash = str(user.password_hash)
    if not verify_password(payload.password, stored_hash):
        raise AppError(401, "INVALID_CREDENTIALS", "Incorrect email or password")


    token = create_access_token(data={"sub": str(user.id)})
    return {"access_token": token, "token_type": "bearer"}


@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user