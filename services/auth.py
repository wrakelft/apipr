import logging

import jwt
import datetime

from fastapi import HTTPException, Security, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials


SECRET_KEY = "sosi_yaitsa"
ALGORITHM = "HS256"
auth_scheme = HTTPBearer()


def create_token(data: dict, expires_delta: datetime.timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.datetime.utcnow() + expires_delta
    else:
        expire = datetime.datetime.utcnow() + datetime.timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_token(token: str):
    try:
        decoded = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return decoded
    except jwt.PyJWTError as e:
        raise HTTPException(status_code=403, detail="Invalid authentication credentials")


def get_current_user(token: HTTPAuthorizationCredentials = Depends(auth_scheme)):
    try:
        payload = decode_token(token.credentials)
        return payload
    except jwt.PyJWTError as e:
        raise HTTPException(status_code=401, detail="Could not validate credentials")


def get_current_user_sub(token: HTTPAuthorizationCredentials = Depends(auth_scheme)):
    try:
        payloadd = decode_token(token.credentials)
        sub = payloadd.get("sub")
        if not sub:
            raise HTTPException(status_code=401, detail="Subject (sub) not found in token")
        return sub
    except jwt.PyJWTError as e:
        raise HTTPException(status_code=401, detail="Could not validate credentials")





