from fastapi import FastAPI
from userCRUD import router as user_router

app = FastAPI()

app.include_router(user_router, prefix="/user")