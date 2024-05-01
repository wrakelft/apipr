import logging

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from database import get_db
from services.auth import create_token, decode_token, auth_scheme, get_current_user

from services import user as UserService
from dto import user as UserDTO

router = APIRouter()


@router.post('/register', tags=["User"])
async def register(data: UserDTO.User = None, db: AsyncSession = Depends(get_db)):
    if data is None:
        raise HTTPException(status_code=400, detail="No user data provided")
    if await UserService.find_user_by_name(data.name, db):
        raise HTTPException(status_code=400, detail="Username already registered")
    user = await UserService.create_user(data, db)
    if user:
        return {"message": "User successfully registered"}
    else:
        raise HTTPException(status_code=500, detail="User registration failed")


@router.get('/{id}', tags=["User"])
async def get(id: int, user: dict = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    return await UserService.get_user(id, db)


# @router.put('/{id}', tags=["User"])
# async def update(data: UserDTO.User = None, id: int = None, db: Session = Depends(get_db)):
#     return UserService.update(data, db, id)


@router.get("/secure-data")
async def secure_data(user: dict = Depends(get_current_user)):
    return {"message": "Secure Data", "user": user}


@router.delete('/remove/{id}', tags=["User"])
async def remove(id: int, user: dict = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    return await UserService.remove(db, id)


@router.post('/auth', tags=["User"])
async def auth(data: UserDTO.User = None, db: AsyncSession = Depends(get_db)):
    if data is None:
        raise HTTPException(status_code=400, detail="No user data provided")
    user = await UserService.auth_user(data, db)
    if user:
        access_token = create_token(data={"sub": data.name})
        return {"access_token": access_token, "token_type": "bearer"}
        # return "You have successfully logged in!"
    else:
        raise HTTPException(status_code=401, detail="Invalid username or password")




