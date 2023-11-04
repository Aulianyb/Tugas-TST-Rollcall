from fastapi import APIRouter
from pydantic import BaseModel
import json

class City(BaseModel):
	id: int
	name : str

router = APIRouter()

city_filename="data/city.json"

with open(city_filename,"r") as read_file:
	city_data = json.load(read_file)
	
@router.get('/')
async def get_all_city(): 
	return city_data['city']

@router.get('/{city_id}')
async def get_city(city_id : int): 
	city_found = False
	for city_iterate in city_data['city']: 
		if city_iterate['id'] == city_id:
			city_found = True
			return city_iterate
	if not city_found: 
		return "Kota tidak ditemukan!"    

@router.post('/')
async def create_city(city: City):
	city_dict = city.dict()
	for city_iterate in city_data['city']: 
		if city_iterate['name'] == city.name or city_iterate['id'] == city.id:
			return "id atau nama kota tersebut sudah ada!"
		
	city_data['city'].append(city_dict)
	with open(city_filename, "w") as write_file: 
		json.dump(city_data, write_file)
	return "Berhasil menambahkan kota"

@router.put('/')
async def update_city(city : City):
	city_dict = city.dict()
	city_found = False 
	for city_iterate in city_data['city']: 
		if city_iterate['name'] == city.name:
			return "Nama kota sudah ada!"
		
	for city_idx, city_iterate in enumerate(city_data['city']): 
		if city_iterate['id'] == city_dict['id']: 
			city_found = True
			city_data['city'][city_idx] = city_dict
			with open(city_filename, "w") as write_file:
				json.dump(city_data, write_file)
			return "Berhasil update kota dengan nama " + city_dict['name']
	if not city_found: 
		return "Kota tidak ditemukan!"

@router.delete("/{city_id}")
async def delete_city(city_id : int): 
	city_found = False
	for city_idx, city_iterate in enumerate(city_data['city']): 
		if city_iterate['id'] == city_id:
			city_found = True
			city_data['city'].pop(city_idx)
			with open(city_filename, "w") as write_file: 
				json.dump(city_data, write_file)
			return "Berhasil menghapus kota"
	if not city_found: 
		return "Kota tidak ditemukan!"