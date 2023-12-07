from fastapi import APIRouter, Depends
from pydantic import BaseModel
import json
from typing import List
from passlib.context import CryptContext
from auth import getCurrentUser
from typing import Annotated

class User(BaseModel):
	id: int
	username: str
	password : str
	boardgame : List[int]
	city : int
	role : str

router = APIRouter()

user_filename="data/user.json"

with open(user_filename,"r") as read_file:
	user_data = json.load(read_file)
	
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password):
    return pwd_context.hash(password)
@router.get('/')

async def get_all_user(currentUser: Annotated[User, Depends(getCurrentUser)]): 
	return user_data['user']

@router.get('/{user_id}')
async def get_user(user_id : int, currentUser: Annotated[User, Depends(getCurrentUser)]): 
	user_found = False
	for user_iterate in user_data['user']: 
		if user_iterate['id'] == user_id:
			user_found = True
			return user_iterate
	if not user_found: 
		return "User tidak ditemukan!"    
	

async def does_username_exist(username : str): 
	user_found = False
	for user_iterate in user_data['user']: 
		if user_iterate['username'] == username:
			user_found = True
			return user_iterate
	if not user_found: 
		return None

@router.post('/')
async def create_user(user: User, currentUser: Annotated[User, Depends(getCurrentUser)]):
	user_dict = user.dict()
	for user_iterate in user_data['user']: 
		if user_iterate['username'] == user.username or user_iterate['id'] == user.id:
			return "Username dan id harus unik!"
	user_dict['boardgame'].sort()

	user_dict['password'] = get_password_hash(user_dict['password'])

	user_data['user'].append(user_dict)
	with open(user_filename, "w") as write_file: 
		json.dump(user_data, write_file)
	return "Berhasil menambahkan user"

@router.put('/')
async def update_user(user : User, currentUser: Annotated[User, Depends(getCurrentUser)]):
	user_dict = user.dict()
	user_found = False 
	
	for user_idx, user_iterate in enumerate(user_data['user']): 
		if user_iterate['id'] == user_dict['id']: 
			user_found = True
			user_dict['password'] = get_password_hash(user_dict['password'])
			user_data['user'][user_idx] = user_dict
			with open(user_filename, "w") as write_file:
				json.dump(user_data, write_file)
			return "Berhasil update user dengan username " + user_dict['username']
	if not user_found: 
		return "User tidak ditemukan!"

@router.delete("/{user_id}")
async def delete_user(user_id : int, currentUser: Annotated[User, Depends(getCurrentUser)]): 
	user_found = False
	for user_idx, user_iterate in enumerate(user_data['user']): 
		if user_iterate['id'] == user_id:
			user_found = True
			user_data['user'].pop(user_idx)
			with open(user_filename, "w") as write_file: 
				json.dump(user_data, write_file)
			return "Berhasil menghapus user"
	if not user_found: 
		return "User tidak ditemukan!"