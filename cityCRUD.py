from fastapi import APIRouter, Depends
from pydantic import BaseModel
from auth import getCurrentUser, User
from typing import Annotated
import json

class City(BaseModel):
	id: int
	name : str

router = APIRouter()

city_filename="data/city.json"

with open(city_filename,"r") as read_file:
	city_data = json.load(read_file)
	
@router.get('/')
async def get_all_city(currentUser: Annotated[User, Depends(getCurrentUser)]): 
	return city_data['city']

@router.get('/{city_id}')
async def get_city(city_id : int, currentUser: Annotated[User, Depends(getCurrentUser)]): 
	city_found = False
	for city_iterate in city_data['city']: 
		if city_iterate['id'] == city_id:
			city_found = True
			return city_iterate
	if not city_found: 
		return "Kota tidak ditemukan!"    