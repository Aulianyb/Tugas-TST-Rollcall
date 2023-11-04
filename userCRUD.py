from fastapi import APIRouter
from pydantic import BaseModel
import json
from typing import List

class User(BaseModel):
	id: int
	username: str
	password : str
	boardgame : List[int]
	city : int

router = APIRouter()

user_filename="data/user.json"

with open(user_filename,"r") as read_file:
	user_data = json.load(read_file)
	
@router.get('/')
async def get_all_user(): 
	return user_data['user']

@router.get('/{user_id}')
async def get_user(user_id : int): 
	user_found = False
	for user_iterate in user_data['user']: 
		if user_iterate['id'] == user_id:
			user_found = True
			return user_iterate
	if not user_found: 
		return "User tidak ditemukan!"    
	
@router.get('/find/')
async def does_username_exist(username : str): 
	user_found = False
	for user_iterate in user_data['user']: 
		if user_iterate['username'] == username:
			user_found = True
			return user_iterate
	if not user_found: 
		return None

@router.post('/')
async def create_user(user: User):
	user_dict = user.dict()
	for user_iterate in user_data['user']: 
		if user_iterate['username'] == user.username or user_iterate['id'] == user.id:
			return "Username dan id harus unik!"
		
	user_data['user'].append(user_dict)
	with open(user_filename, "w") as write_file: 
		json.dump(user_data, write_file)
	return "Berhasil menambahkan user"

@router.put('/')
async def update_user(user : User):
	user_dict = user.dict()
	user_found = False 
	for user_iterate in user_data['user']: 
		if user_iterate['username'] == user.username:
			return "Username sudah ada!"
	
	for user_idx, user_iterate in enumerate(user_data['user']): 
		if user_iterate['id'] == user_dict['id']: 
			user_found = True
			user_data['user'][user_idx] = user_dict
			with open(user_filename, "w") as write_file:
				json.dump(user_data, write_file)
			return "Berhasil update user dengan username " + user_dict['username']
	if not user_found: 
		return "User tidak ditemukan!"

@router.delete("/{user_id}")
async def delete_user(user_id : int): 
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