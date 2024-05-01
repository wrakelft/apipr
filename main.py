import uvicorn
from fastapi import FastAPI
from database import SessionLocal, engine, Base, create_tables
from routers import user as UserRouter
from routers import files as FileRouter


app = FastAPI()
app.include_router(UserRouter.router, prefix="/user")
app.include_router(FileRouter.router, prefix="/files")


@app.on_event("startup")
async def startup_event():
    await create_tables(engine)

if __name__ == '__main__':
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True, workers=3)




