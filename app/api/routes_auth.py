from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, status, Header

from pydantic import BaseModel

from app.auth import pwd_manager
from app.db.database import SessionLocal
from app.models.users import User
from app.auth.token_manager import create_access_token, validate_token, active_tokens
from app.models.auth import LoginRequest

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class UserCreate(BaseModel):
    username: str
    password: str

@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.username == user.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")
    
    hashed_password = pwd_manager.hash_password(user.password)

    new_user = User(username=user.username, hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "User registered successfully", "username": new_user.username}

@router.post("/login")
def login(request: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == request.username).first()
    if not user or not pwd_manager.verify_password(request.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    if request.username in  active_tokens:
        return {"access_token": active_tokens[request.username], "token_type": "bearer"}
    
    access_token = create_access_token(data={"sub": request.username})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/validate-token")
def validate_token_route(authorization: str = Header(...)):
    token = authorization.replace("Bearer ", "")
    user = validate_token(token)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    return {"message": "Token is valid", "user": user}