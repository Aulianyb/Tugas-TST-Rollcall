from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from datetime import datetime, timedelta
from typing import Annotated
from typing import List
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import json
from passlib.context import CryptContext
from jose import JWTError, jwt

class User(BaseModel):
	id: int
	username: str
	password : str
	boardgame : List[int]
	city : int
	role : str

SECRET_KEY = "2f8d9e786d50a6c7e23fd8a19406df9c6933f9f6a9a07e312b3692b6e8cf61f3"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

class User_auth(BaseModel):
	username: str
	password : str

class Token(BaseModel):
	access_token: str
	token_type: str

class TokenData(BaseModel):
	username: str or None = None


router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
credentials_exception = HTTPException(
	status_code=status.HTTP_401_UNAUTHORIZED,
	detail="Could not validate credentials",
	headers={"WWW-Authenticate": "Bearer"},
)

user_filename="data/user.json"
with open(user_filename,"r") as read_file:
	user_data = json.load(read_file)

def get_password_hash(password):
    return pwd_context.hash(password)
@router.get('/')

async def does_username_exist(username : str): 
	user_found = False
	for user_iterate in user_data['user']: 
		if user_iterate['username'] == username:
			user_found = True
			return user_iterate
	if not user_found: 
		return None
	
@router.post('/register')
async def create_user(user: User):
	user_dict = user.dict()
	for user_iterate in user_data['user']: 
		if user_iterate['username'] == user.username or user_iterate['id'] == user.id:
			return "Username dan id harus unik!"
	user_dict['boardgame'].sort()

	user_dict['password'] = get_password_hash(user_dict['password'])

	user_data['user'].append(user_dict)
	with open(user_filename, "w") as write_file: 
		json.dump(user_data, write_file)
	return user

def verify_password(plain_password, hashed_password):
	return pwd_context.verify(plain_password, hashed_password)

async def authenticate_user(username: str, password: str):
	user = await does_username_exist(username) 
	if not user:
		return False
	if not verify_password(password, user['password']):
		return False
	return user

def create_access_token(data: dict, expires_delta: timedelta or None = None):
	to_encode = data.copy()
	if expires_delta:
		expire = datetime.utcnow() + expires_delta
	else:
		expire = datetime.utcnow() + timedelta(minutes=15)
	to_encode.update({"exp": expire})
	encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
	return encoded_jwt

async def getCurrentUser(token: Annotated[str, Depends(oauth2_scheme)]):
	try:
		payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
		username: str = payload.get("sub")
		if username is None:
			raise credentials_exception
		token_data = TokenData(username=username)
	except JWTError:
		raise credentials_exception
	user = await does_username_exist(token_data.username)
	if user is None:
		raise credentials_exception
	return user

@router.get("/")
async def welcomePage():
	return "Welcome to RollCall API Services!"

@router.post("/token")
async def loginAuth(form_data : Annotated[OAuth2PasswordRequestForm, Depends()]):
	fetched_user = await authenticate_user(form_data.username, form_data.password)
	if not fetched_user: 
		raise HTTPException(
			status_code=status.HTTP_401_UNAUTHORIZED,
			detail="Incorrect username or password",
			headers={"WWW-Authenticate": "Bearer"},
		)
	
	access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
	access_token = create_access_token(
		data={"sub": fetched_user['username']}, expires_delta=access_token_expires
	)
	return {"access_token": access_token, "token_type": "bearer"}

@router.get("/users/me")
async def read_users_me(
	current_user: Annotated[User, Depends(getCurrentUser)]
):
	return current_user

@router.get('/user')
async def get_all_user(): 
	return user_data['user']

@router.get('/user/{user_id}')
async def get_user(user_id : int): 
	user_found = False
	for user_iterate in user_data['user']: 
		if user_iterate['id'] == user_id:
			user_found = True
			return user_iterate
	if not user_found: 
		return "User tidak ditemukan!"  


@router.put('/user')
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

@router.delete("/user/{user_id}")
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