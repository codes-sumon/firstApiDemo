from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from models.user import User
from schemas.user import UserCreate, UserResponse, UserLogin
from utils.jwt_handler import create_access_token, verify_token, create_refresh_token
from fastapi import Body
from fastapi import Form
import bcrypt


router = APIRouter(prefix="/auth", tags=["Authentication"])

# Database dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 🔹 Register
@router.post("/register", response_model=UserResponse)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.username == user.username).first()
    if existing:
        raise HTTPException(status_code=400, detail="Username already exists")
    
    hashed_pw = bcrypt.hashpw(user.password.encode("utf-8"), bcrypt.gensalt())
    db_user = User(username=user.username, email=user.email, hashed_password=hashed_pw.decode())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# 🔹 Login
@router.post("/login")
def login(username: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == username).first()
    if not db_user or not bcrypt.checkpw(password.encode("utf-8"), db_user.hashed_password.encode("utf-8")):
        raise HTTPException(status_code=401, detail="Invalid username or password")
    
    access_token = create_access_token({"sub": db_user.username})
    refresh_token = create_refresh_token({"sub": db_user.username})
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }

@router.post("/refresh")
def refresh_token(refresh_token: str = Body(...)):
    username = verify_token(refresh_token)
    if not username:
        raise HTTPException(status_code=401, detail="Invalid or expired refresh token")
    
    new_access_token = create_access_token({"sub": username})
    return {"access_token": new_access_token, "token_type": "bearer"}

# 🔹 Protected route example
# @router.get("/me")
# def read_profile(token: str, db: Session = Depends(get_db)):
#     username = verify_token(token)
#     if not username:
#         raise HTTPException(status_code=401, detail="Invalid or expired token")
#     user = db.query(User).filter(User.username == username).first()
#     return {"username": user.username, "email": user.email}

