from fastapi import APIRouter, HTTPException, status
from models.schemas import UserCreate, UserLogin, Token, UserResponse
from utils.auth import get_password_hash, verify_password, create_access_token
from database import execute_query
from sqlalchemy import text
from database import engine
from datetime import datetime

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", response_model=Token, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserCreate):
    with engine.connect() as conn:
        existing_user = conn.execute(
            text("SELECT id FROM users WHERE email = :email"),
            {"email": user_data.email}
        ).fetchone()

        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )

        hashed_password = get_password_hash(user_data.password)

        result = conn.execute(
            text("""
                INSERT INTO users (email, password_hash, full_name, created_at, updated_at)
                VALUES (:email, :password_hash, :full_name, :created_at, :updated_at)
                RETURNING id, email, full_name, created_at
            """),
            {
                "email": user_data.email,
                "password_hash": hashed_password,
                "full_name": user_data.full_name,
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            }
        )
        conn.commit()

        user = result.fetchone()

        access_token = create_access_token(data={"sub": str(user.id)})

        user_response = UserResponse(
            id=str(user.id),
            email=user.email,
            full_name=user.full_name,
            created_at=user.created_at
        )

        return Token(
            access_token=access_token,
            token_type="bearer",
            user=user_response
        )

@router.post("/login", response_model=Token)
async def login(credentials: UserLogin):
    with engine.connect() as conn:
        result = conn.execute(
            text("SELECT id, email, password_hash, full_name, created_at FROM users WHERE email = :email"),
            {"email": credentials.email}
        )
        user = result.fetchone()

        if not user or not verify_password(credentials.password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        access_token = create_access_token(data={"sub": str(user.id)})

        user_response = UserResponse(
            id=str(user.id),
            email=user.email,
            full_name=user.full_name,
            created_at=user.created_at
        )

        return Token(
            access_token=access_token,
            token_type="bearer",
            user=user_response
        )
