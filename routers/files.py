
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from services.file import save_file
from services.auth import get_current_user, get_current_user_sub
from services.user import get_user_id_by_name


router = APIRouter()


@router.post("/upload")
async def upload_file(file: UploadFile = File(...), sub: str = Depends(get_current_user_sub), user: dict = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    user_id = await get_user_id_by_name(sub, db)
    result = await save_file(file, user_id, db)
    return result

