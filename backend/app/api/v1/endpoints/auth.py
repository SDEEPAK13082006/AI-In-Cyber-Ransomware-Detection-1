"""
API v1 - Authentication Endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend.app.core.database import get_db
from backend.app.core.security import verify_password, create_access_token, get_password_hash
from backend.app.schemas.auth import UserLoginSchema, UserCreateSchema, TokenSchema, UserResponseSchema
from backend.app.models.db.user import User

router = APIRouter()

@router.post("/login", response_model=TokenSchema)
def login_for_access_token(user_credentials: UserLoginSchema, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == user_credentials.username).first()
    
    # If initial user doesn't exist, auto-create default admin account for easy initial evaluation
    if not user and user_credentials.username == "AdminAnalyst":
        hashed_pwd = get_password_hash("admin123")
        user = User(username="AdminAnalyst", email="admin@defender.cyber", hashed_password=hashed_pwd, role="admin")
        db.add(user)
        db.commit()
        db.refresh(user)

    if not user or not verify_password(user_credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(subject=user.username, role=user.role)
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "username": user.username,
        "role": user.role
    }

@router.post("/register", response_model=UserResponseSchema, status_code=status.HTTP_201_CREATED)
def register_user(user_in: UserCreateSchema, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.username == user_in.username).first()
    if existing:
        raise HTTPException(status_code=400, detail="Username already registered")

    user = User(
        username=user_in.username,
        email=user_in.email,
        hashed_password=get_password_hash(user_in.password),
        role=user_in.role or "analyst"
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
