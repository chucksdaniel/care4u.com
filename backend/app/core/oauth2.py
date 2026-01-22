from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from datetime import datetime, timedelta
from sqlalchemy.orm import Session

from app.core.db_session import get_db
from app.models import User
from app.schemas.user import TokenData
from app.enum import UserRole
from app.core import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES

def create_access_token(data: dict):
    # Copy the data to encode so that we don't modify the original
    to_encode = data.copy()
    # Here you would add expiration time to the token if needed
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: str = payload.get("user_id")
        if id is None:
            raise credentials_exception
        token_data = TokenData(id=id)
        # return token_data
    except JWTError:
        raise credentials_exception
        # raise HTTPException(status_code=401, detail="Invalid token")
    return token_data

""" Get the current user logged in """    
def get_current_user(
        token: str = Depends(oauth2_scheme), 
        db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    token = verify_access_token(token, credentials_exception)
    user = db.query(User).filter(User.id == token.id).first()

    return user

""" Get the current admin user logged in """
def get_current_admin_user(
        token: str = Depends(oauth2_scheme), 
        db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    token = verify_access_token(token, credentials_exception)
    user = db.query(User).filter(User.id == token.id).first()

    if not user.role == "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform this action")

    return user

""" General role-based access control dependency """
def require_roles(*allowed_roles: UserRole):
    def role_checker(current_user: User = Depends(get_current_user)):
        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions"
            )
        return current_user
    return role_checker

""" Specific role-based access control dependency method 2"""
def require_role(role_name: str):
    def checker(user=Depends(get_current_user)):
        if role_name not in [r.name for r in user.roles]:
            raise HTTPException(status_code=403)
        return user
    return checker