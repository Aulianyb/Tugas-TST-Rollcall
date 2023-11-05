from fastapi import APIRouter
from pydantic import BaseModel
import json

class Boardgame(BaseModel):
	id: int
	name : str

router = APIRouter()

boardgame_filename="data/boardgame.json"

with open(boardgame_filename,"r") as read_file:
	boardgame_data = json.load(read_file)
	
@router.get('/')
async def get_all_boardgame(): 
	return boardgame_data['boardgame']

@router.get('/{boardgame_id}')
async def get_boardgame(boardgame_id : int): 
	boardgame_found = False
	for boardgame_iterate in boardgame_data['boardgame']: 
		if boardgame_iterate['id'] == boardgame_id:
			boardgame_found = True
			return boardgame_iterate
	if not boardgame_found: 
		return "Boardgame tidak ditemukan!"    

@router.post('/')
async def create_boardgame(boardgame: Boardgame):
	boardgame_dict = boardgame.dict()
	for boardgame_iterate in boardgame_data['boardgame']: 
		if boardgame_iterate['name'] == boardgame.name or boardgame_iterate['id'] == boardgame.id:
			return "id atau nama boardgame tersebut sudah ada!"
		
	boardgame_data['boardgame'].append(boardgame_dict)
	with open(boardgame_filename, "w") as write_file: 
		json.dump(boardgame_data, write_file)
		return "Berhasil menambahkan boardgame"

@router.put('/')
async def update_boardgame(boardgame : Boardgame):
	boardgame_dict = boardgame.dict()
	boardgame_found = False 
	for boardgame_iterate in boardgame_data['boardgame']: 
		if boardgame_iterate['name'] == boardgame.name:
			return "Nama boardgame sudah ada!"
		
	for boardgame_idx, boardgame_iterate in enumerate(boardgame_data['boardgame']): 
		if boardgame_iterate['id'] == boardgame_dict['id']: 
			boardgame_found = True
			boardgame_data['boardgame'][boardgame_idx] = boardgame_dict
			with open(boardgame_filename, "w") as write_file:
				json.dump(boardgame_data, write_file)
			return "Berhasil update boardgame dengan nama " + boardgame_dict['name']
	if not boardgame_found: 
		return "Boardgame tidak ditemukan!"

@router.delete("/{boardgame_id}")
async def delete_boardgame(boardgame_id : int): 
	boardgame_found = False
	for boardgame_idx, boardgame_iterate in enumerate(boardgame_data['boardgame']): 
		if boardgame_iterate['id'] == boardgame_id:
			boardgame_found = True
			boardgame_data['boardgame'].pop(boardgame_idx)
			with open(boardgame_filename, "w") as write_file: 
				json.dump(boardgame_data, write_file)
			return "Berhasil menghapus boardgame"
	if not boardgame_found: 
		return "Boardgame tidak ditemukan!"