from fastapi import APIRouter
from pydantic import BaseModel
from userCRUD import User, does_username_exist
import json

class User_auth(BaseModel):
	username: str
	password : str

router = APIRouter()

auth_filename="data/auth.json"
with open(auth_filename,"r") as read_file:
	auth_data = json.load(read_file)

@router.get("/currentUser")
async def getCurrentUser():
	return auth_data['auth']

@router.post("/login")
async def login(user_auth : User_auth):
	if await getCurrentUser() != [] : 
		return "Sudah ada user yang log in, harap log out terlebih dahulu"
	fetched_user = await does_username_exist(user_auth.username)
	if fetched_user != None: 
		if fetched_user['password'] == user_auth.password: 
			auth_data['auth'].append(fetched_user)
			with open(auth_filename, "w") as write_file: 
				json.dump(auth_data, write_file)
			return "Berhasil login"
	return "Gagal login"

@router.delete("/logout")
async def logout():
	if await getCurrentUser() == [] : 
		return "Tidak ada user yang logged in, harap log in terlebih dahulu"
	auth_data['auth'].pop()
	with open(auth_filename, "w") as write_file: 
		json.dump(auth_data, write_file)
	return "Berhasil logout"