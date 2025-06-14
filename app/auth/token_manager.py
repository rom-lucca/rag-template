import os
from datetime import datetime, timedelta
from typing import Optional, Dict

from jose import jwt

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

active_tokens: Dict[str, str] = {}

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    
    expire = datetime.utcnow() + (expires_delta if expires_delta else timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    username = data.get("sub")
    if username:
        active_tokens[username] = encoded_jwt
    
    return encoded_jwt

def validate_token(token: str) -> Optional[dict]:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            return None
        
        if active_tokens.get(username) != token:
            return None
        
        return username
    
    except jwt.ExpiredSignatureError:
        return None
    except jwt.JWTError:
        return None
    except Exception as e:
        raise ValueError(f"An error occurred while validating the token: {str(e)}")

def remove_token(username: str) -> None:
    """Remove a token for a specific user."""
    if username in active_tokens:
        del active_tokens[username]

def get_active_token(username: str) -> Optional[str]:
    """Get all active tokens."""
    return active_tokens.get(username)