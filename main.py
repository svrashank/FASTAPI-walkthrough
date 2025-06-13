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