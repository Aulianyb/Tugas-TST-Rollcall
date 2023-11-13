from fastapi import APIRouter, Depends
from typing import Annotated
from auth import getCurrentUser
from userCRUD import get_user, User
from typing import List
import json

router = APIRouter()
user_filename="data/user.json"

with open(user_filename,"r") as read_file:
	user_data = json.load(read_file)

def how_many_similarities(arr1 : List[int], arr2 : List[int]):
    max = List[int]
    min = List[int]
    if len(arr1) >= len(arr2):
        max = arr1
        min = arr2
    else: 
        min = arr2
        max = arr1
    
    count = 0
    max_idx = 0
    min_idx = 0
    if max == [] or min == [] : 
        return 0
    
    while max[max_idx] < min[min_idx] and (max_idx < len(max)):
        max_idx+=1
    
    while ((max_idx < len(max)) and (min_idx < len(min))): 
        if max[max_idx] == min[min_idx] : 
            count += 1
            max_idx += 1
            min_idx += 1
        elif max[max_idx] > min[min_idx]: 
            min_idx+= 1
        else: 
            max_idx += 1
    return count
        
        
             

@router.get('/')
async def matchmaking(currentUser: Annotated[User, Depends(getCurrentUser)]):
    matchmaker = []
    if currentUser == []: 
        return "Tidak ada user yang logged in, harap logged in terlebih dahulu"

    for user_iterate in user_data['user']:
        if user_iterate['city'] == currentUser['city'] and user_iterate['id'] != currentUser['id']: 
            similar_boardgame = how_many_similarities(user_iterate['boardgame'], currentUser['boardgame'])
            if similar_boardgame > 0 : 
                matchmaker.append([user_iterate['id'], similar_boardgame])
    matchmaker = sorted(matchmaker, key=lambda x: x[1], reverse=True)
    
    matchmaker_result = []
    if matchmaker == []: 
        return "Maaf, sepertinya tidak ada player lain yang cocok denganmu :("
    for player in matchmaker:
        fetched_player = await get_user(player[0])
        matchmaker_result.append([fetched_player, "kamu punya " + str(player[1]) + " kesamaan dalam minat boardgame dengan user ini!"])
    return matchmaker_result