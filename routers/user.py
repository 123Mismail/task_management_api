from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from database.database import get_session
from models.user import User as UserModel
from schemas.user import UserCreate, UserResponse
from pwdlib import PasswordHash
from pwdlib.hashers.argon2 import Argon2Hasher

router = APIRouter(prefix="/users", tags=["users"])

def get_password_hasher():
    """Configure pwdlib with Argon2 algorithm for secure password hashing"""
    return PasswordHash([Argon2Hasher(
        time_cost=3,
        memory_cost=65536,
        parallelism=1,
        hash_len=32,
        salt_len=16,
    )])

def hash_password(plain_password: str):
    ph = get_password_hasher()
    return ph.hash(plain_password)

@router.post("/signup", response_model=UserResponse, status_code=201)
async def signup_user(user_create: UserCreate, db: Session = Depends(get_session)):
    existing_user = db.query(UserModel).filter(UserModel.email == user_create.email).first()
    if existing_user:
        raise HTTPException(status_code=409, detail="Email already registered")

    # Hash the password
    hashed_password = hash_password(user_create.password)

    # Create user in database
    db_user = UserModel(
        email=user_create.email,
        first_name=user_create.first_name,
        last_name=user_create.last_name,
        hashed_password=hashed_password
    )

    try:
        db.add(db_user)
        db.commit()
        db.refresh(db_user)

        # Create response object separately to catch potential serialization errors
        response = UserResponse(
            id=db_user.id,
            email=db_user.email,
            first_name=db_user.first_name,
            last_name=db_user.last_name,
            created_at=db_user.created_at
        )
        return response

    except Exception:
        # Rollback the transaction if there's any error during response creation
        db.rollback()
        raise HTTPException(status_code=500, detail="Error occurred during user creation")
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Email already registered")