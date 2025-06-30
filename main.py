from fastapi import FastAPI, Query

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}

# Cannot redefine a path. 
# @app.get("/item/{item_name}")
# async def item(item_name:int):
#     return {"message":item_name}

# Order matters because if the following function was placed below the next function them the api would return {"message":"me"}
@app.get("/item/me")
async def item():
    return {"message":"This is my own profile"}

#Path Parameters with Type
@app.get("/item/{item_name}")
async def item(item_name:int):
    return {"message":item_name}

# You can define what values or types should be in the path parameters 
from enum import Enum
# Here we define a class and enter the type of the path paramter
class Rhyme(str, Enum):
    thyme = "rhyme"
    fall = "ball"
    target = "forget"

@app.get("/rhyme/{rhyme}")
async def rhyme(rhyme:Rhyme):
    if rhyme.value == "ball":
        return {"message":f"Your rhyming word is {Rhyme.fall}"}
    if rhyme.value == "forget":
        return {"message":f"Your rhyming word is {Rhyme.forget}"}
    return {"message":f"{rhyme.value} is not stored in our Class"}



# Query Paramters 
# in the request http://127.0.0.1:8000/items/?skip=0&limit=10m  anything after a ? is a query parameter
# You can have defaults in query parameter and they can accessed when they are set , but otherwise they will be invisible. 
# So ?skip=0&limit=10 can be set as default and it won't show in the request

# Lets construct a response from an orm call to the db
fake_db = [
    {"emp_name": "Vrashank", "location": "Mulund", "position": "Founder and CEO"},
    {"emp_name": "Aisha Khan", "location": "Bandra", "position": "Chief Technology Officer"},
    {"emp_name": "Rohan Mehta", "location": "Andheri", "position": "Software Engineer"},
    {"emp_name": "Sneha Patil", "location": "Thane", "position": "Product Manager"},
    {"emp_name": "Aditya Sharma", "location": "Powai", "position": "Data Scientist"},
    {"emp_name": "Priya Desai", "location": "Borivali", "position": "UX Designer"},
    {"emp_name": "Kunal Joshi", "location": "Goregaon", "position": "Backend Developer"},
    {"emp_name": "Meera Iyer", "location": "Vikhroli", "position": "HR Manager"},
    {"emp_name": "Devansh Shah", "location": "Dadar", "position": "DevOps Engineer"},
    {"emp_name": "Ritika Kapoor", "location": "Colaba", "position": "Marketing Lead"}
]

# Here I am setting the founders CEO and CTO as default for the function get_founders. You can also pass optional parameters
# By setting them to None 
# You can set path and query parameters in a single function FASTAPI can differentiate between them, emp_name is a path param set to None by default
# Just Don't set the default value if you want to make a query parameter mandatory
from typing import List
# @app.get("/founders/{emp_name}")
# async def get_founders(emp_name: str | None = None, position : List[str] = Query(default=["Founder and CEO", "Chief Technology Officer"], location: str | None  = None)):
#     founders = []
#     for emp in fake_db:
#         if emp.get("position") in position:
#             founders.append(emp)
#     return founders

# Setting multiple query paramaters in a Model
from typing import Annotated, Literal

from fastapi import FastAPI, Query, Body
from pydantic import BaseModel, Field

class DefaultFilters(BaseModel):
    position : List[str] = Query (default = ["Founder and CEO", "Chief Technology Officer"])

@app.get("/mode_default_founders")
async def get_model_founders( position : Annotated[DefaultFilters,Query()]):
    founders = []
    for emp in fake_db:
        if emp.get("position") in position:
            founders.append(emp)
    return founders


# The json payload that you will send in the post request can also be declared using Pydantic
class Employee(BaseModel):
    emp_name :str | None = None 
    age : int = Body(25)


### Body Parameters 
@app.post("/employees/")
async def post_employee_info(emp: Employee):
    return {"Employee":emp}


## You can Declare validation for each field of the json 
from pydantic import Field 
class Employee(BaseModel):
    emp_name :str | None = Field(max_length = 200)
    age : int = Body(25)


### Body Parameters 
@app.post("/employees_validated/")
async def post_employee_info(emp: Employee):
    return {"Employee":emp}


# you can nest your modules 
from pydantic import HttpUrl
class Job(BaseModel):
    designation : str | None = None 
    employee : Employee | None = None 
    linkedin : HttpUrl


@app.post("/job/")
async def get_job(job: Job):
    job = {
        "designation": "Full Stack Developer",
        "employee" : {
            "emp_name" : "Vrashank Shetty",
            "age" : 29
        },
        "linkedin": "https://in.linkedin.com/"
    }
    return {"job":job}

# You can declare a Body, Query or path parameter with an example
from pydantic import HttpUrl
class Job(BaseModel):
    designation : str | None = None 
    employee : Employee | None = None 
    linkedin : HttpUrl

from fastapi import Body
@app.post("/job/")
async def get_job(job: Annotated [Job, Body ( examples = [{"designation": "Enter Designation Here","employee" : {"emp_name" : "Employee Name","age" : 29},"linkedin": "https://in.linkedin.com/"}])]):
    job = {
            "designation": "Full Stack Developer",
            "employee" : {
                "emp_name" : "Vrashank Shetty",
                "age" : 29
            },
            "linkedin": "https://in.linkedin.com/"
        }
    return {"job":job}



from fastapi import Header, Cookie

@app.get("/item_name/")
async def get_item_name(headers: Annotated [str | None, Header(convert_underscore = True) ] = None):
    return headers

# You can extra duplicate values of a header using list[str]
# FASTAPI will take care of converting _ to - or vice versa
# from fastapi import Header, Cookie

# @app.get("/item_name/")
# async def get_item_name(x_token: Annotated [list[str] | None, Header(convert_underscore = True) ] = None):
#     return headers

# You can pass a header format 

class DefaultHeaders(BaseModel):
    client_id : str | None = None
    client_secret :str | None = Field(max_length = 20)
    keep_alive : bool | None = Field(default = True)

@app.post("/item_name_with_headers/")
async def get_item_name_with_headers(headers : Annotated[DefaultHeaders, Header()]):
    return headers



# Models and their example 
from pydantic import EmailStr

class UserIn(BaseModel):
    fullname :str | None = None 
    email :EmailStr 
    password: Annotated[str, Field(mandatory= True)]


class UserOut(BaseModel):
    fullname : str | None = None 
    email : EmailStr

class UserInDB(BaseModel):
    fullname : str | None = None
    hashed_password : str 
    email : EmailStr


def hash_password(password:str) -> str:
    return "hash" + password

def fake_save_user(user_in: UserIn):
    hashed_password = fake_password_hasher(user_in.password)
    user_in_db = UserInDB(**user_in.dict(), hashed_password=hashed_password)

@app.post("/user/",response_model = UserOut)
async def create_user(user_info: UserIn) :
    fake_save_user(user_in)


# Security 
# from typing import Annotated

# from fastapi import Depends, FastAPI
# from fastapi.security import OAuth2PasswordBearer

# app = FastAPI()

# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# @app.get("/items/")
# async def read_items(token: Annotated[str, Depends(oauth2_scheme)]):
#     return {"token": token}
    

# # Following is how you would return a user from the DB
# from typing import Annotated

# from fastapi import Depends, FastAPI, HTTPException, status
# from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
# from pydantic import BaseModel

# fake_users_db = {
#     "johndoe": {
#         "username": "johndoe",
#         "full_name": "John Doe",
#         "email": "johndoe@example.com",
#         "hashed_password": "fakehashedsecret",
#         "disabled": False,
#     },
#     "alice": {
#         "username": "alice",
#         "full_name": "Alice Wonderson",
#         "email": "alice@example.com",
#         "hashed_password": "fakehashedsecret2",
#         "disabled": True,
#     },
# }

# class User(BaseModel):
#     username : str | None = None
#     full_name : str | None = None
#     email : str | None = None 
#     disabled : bool | None = None

# class UserInDB(User):
#     hashed_password : str | None = None 

# def hash_password(password: str):  # Renamed
#     return "fakehashed" + password

# oauth2_scheme = OAuth2PasswordBearer(tokenUrl = "token")

# def get_user(db, username :str):
#     if username in db :
#         # get the user in the dict
#         user_dict = db.get(username)
#         # Following is as good as passing arguments as key = value from the dict
#         return UserInDB(**user_dict)
# def get_user_from_token(token: str):
#     user = get_user(fake_users_db, token)
#     return user

# async def get_current_user(token : Annotated[str, Depends(oauth2_scheme)]):
#     user  = get_user_from_token(token)
#     if not user:
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Invalid authentication credentials",
#             headers={"WWW-Authenticate": "Bearer"})
#     return user

# async def get_active_user(user : Annotated[User, Depends(get_current_user)]):
#     if user.disabled:
#         raise HTTPException(status_code=400, detail="Inactive user") 
#     return user 

# @app.post("/token")
# async def login(form_data : Annotated[OAuth2PasswordRequestForm, Depends()]):
#     username = form_data.username
#     user_in_db = get_user(fake_users_db,username)
#     if not user_in_db:
#         raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,detail = f"User {username} not found")
#     hashed_password = user_in_db.hashed_password
#     hashed_form_password = hash_password(form_data.password)
#     if hashed_password != hashed_form_password:
#         raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED,
#                 detail="Invalid login credentials",headers={"WWW-Authenticate": "Bearer"})
#     return {"access_token": user_in_db.username, "token_type": "bearer"}


# @app.get('/users/me')
# async def get_current_session_user(current_user : Annotated[User,Depends(get_active_user)]):
#     return current_user


#Security with Jwt 

from datetime import datetime, timedelta, timezone
from typing import Annotated

import jwt
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext
from pydantic import BaseModel

SECRET = "27af804ea264e867c81c23a928749fb44993f61e610059459c580431f35523be"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
        "disabled": False,
    }
}

class Token(BaseModel):
    access_token : str | None = None
    token_type : str | None = None

class TokenData(BaseModel):
    username : str | None = None

class User(BaseModel):
    username : str | None = None
    full_name : str | None = None
    email : str | None = None 
    disabled : bool | None = None
   
class UserInDB(User):
    hashed_password : str | None = None

# Hashing algo
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
# Getting token url from the request
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def verify_password(plain_text_password,hashed_db_password):
    return pwd_context.verify(plain_text_password,hashed_db_password)

def get_password_hash(password : str) -> str :
    return pwd_context.hash(password)

def get_user(username : str, fake_db: dict):
    if username not in fake_db:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,detail = f"User {username} not found",headers={"WWW-Authenticate": "Bearer"})
    user = fake_db.get(username)
    return UserInDB(**user)

def authenticate_user(fake_db, username : str, password :str ):
    user = get_user(username,fake_db)
    if not verify_password(password,user.hashed_password):
        return False
    return True

def create_access_token(data:dict,expires_delta : timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        access_token_expires_in = datetime.now(timezone.utc) + expires_delta
    else:
        access_token_expires_in = datetime.now(timezone.utc) + timedelta(minutes = 15)
    to_encode.update({"exp":access_token_expires_in})
    encoded_jwt  = jwt.encode(to_encode,SECRET,algorithm = ALGORITHM)
    return encoded_jwt 

async def get_current_user(token : Annotated[str,Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    user = None
    try:
        payload = jwt.decode(token,SECRET,algorithm = ALGORITHM)
        username = payload.get("sub")
        if not username:
            raise credentials_exception
        token_date = TokenData(username)
        user = get_user(token_date.username,fake_db)
    except InvalidTokenError:
        raise credentials_exception
    if not user:
        raise credentials_exception
    return user

def get_current_active_user(current_user: Annotated[User,Depends(get_current_user)]):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

@app.post("/token")
async def login_for_access_token(form_data : Annotated[OAuth2PasswordRequestForm, Depends()]) -> Token :
    user = authenticate_user(fake_db,form_data.username,form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"})
    expires_delta = timedelta(minutes = ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token({"sub":form_data.username},expires_delta)
    return Token(access_token=access_token,token_type = "Bearer")

@app.get("/users/me",response_model = User)
async def get_logged_in_user(current_user: Annotated[User,Depends(get_active_user)]):
    return current_user


    
    