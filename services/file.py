from pathlib import Path

from fastapi import UploadFile, HTTPException
from sqlalchemy import select
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import FileResponse


from models.files import File

import aiofiles

BASE_DIR = Path(__file__).resolve().parent
UPLOAD_DIR = BASE_DIR/'uploads'
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


async def save_file(upload_file: UploadFile, user_id: int, db: AsyncSession):
    file_location = UPLOAD_DIR/upload_file.filename
    async with aiofiles.open(file_location, "wb") as file_object:
        file_content = await upload_file.read()
        await file_object.write(file_content)

    db_file = File(file_name=upload_file.filename, user_id=user_id)
    db.add(db_file)
    await db.commit()
    await db.refresh(db_file)

    return {"info": f"File '{upload_file.filename}' , db id: {db_file.id}"}


async def load_file(file_id: int, db: AsyncSession):
    try:
        async with db.begin_nested():
            query = select(File).filter(File.id == file_id)
            result = await db.execute(query)
            db_file = result.scalars().first()

        if db_file is None:
            raise HTTPException(status_code=404, detail="File not found")

        file_path = UPLOAD_DIR/db_file.file_name
        if not file_path.exists():
            raise HTTPException(status_code=404, detail="File not found on disk")

        return FileResponse(path=file_path, filename=db_file.file_name)
    except InvalidRequestError:
        raise HTTPException(status_code=406, detail="error")


async def check_owner(user_id: int, file_id: int, db: AsyncSession):
    query = select(File).filter(File.id == file_id, File.user_id == user_id)
    result = await db.execute(query)
    file_record = result.scalars().first()
    return file_record is not None




