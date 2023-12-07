from fastapi import FastAPI
from userCRUD import router as user_router
from cityCRUD import router as city_router
from boardgameCRUD import router as boardgame_router
from boardgameCRUD import router as boardgame_router
from auth import router as auth_router
from matchmaking import router as matchmaking_router
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

app.add_middleware(
  CORSMiddleware,
  allow_origins=["http://localhost:5173"],
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"],
)

app.include_router(user_router, prefix="/user")
app.include_router(city_router, prefix="/city")
app.include_router(boardgame_router, prefix="/boardgame")
app.include_router(auth_router, prefix="")
app.include_router(matchmaking_router, prefix="/matchmaking")
