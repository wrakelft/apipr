from pathlib import Path

from fastapi import UploadFile
from sqlalchemy.ext.asyncio import AsyncSession


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

    return {"info": f"File '{upload_file.filename}' saved at '{file_location}', db id: {db_file.id}"}




