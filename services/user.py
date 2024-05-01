import bcrypt
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from models.user import User
from dto import user


async def create_user(data: user.User, db: AsyncSession):
    user = User(name=data.name, email=data.email, password=hash_password(data.password))
    try:
        db.add(user)
        await db.commit()
        await db.refresh(user)
    except Exception as e:
        print(e)

    return user


async def auth_user(data: user.User, db: AsyncSession):
    user = await db.execute(
        select(User).where(User.name == data.name)
    )
    user = user.scalars().first()
    if user and verify_password(data.password, user.password):
        return True
    return False


async def get_user(id: int, db: AsyncSession):
    result = await db.execute(
        select(User).where(User.id == id)
    )
    return result.scalars().first()


async def get_user_id_by_name(name: str, db: AsyncSession):
    result = await db.execute(
        select(User.id).where(User.name == name)
    )
    user_id = result.scalars().first()
    return user_id


async def find_user_by_name(name: str, db: AsyncSession):
    result = await db.execute(
        select(User).where(User.name == name)
    )
    user = result.scalars().first()
    if user:
        return True
    return False


# def update(data: user.User, db: Session, id: int):
#     user = db.query(User).filter(User.id == id).first()
#     user.name = data.name
#     db.add(user)
#     db.commit()
#     db.refresh(user)
#
#     return user


async def remove(db: AsyncSession, id: int):
    await db.execute(
        delete(User).where(User.id == id)
    )
    await db.commit()
    return {"message": "User deleted"}


def hash_password(password):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password


def verify_password(password, hashed_password):
    if isinstance(hashed_password, str):
        hashed_password = hashed_password.encode('utf-8')
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)







