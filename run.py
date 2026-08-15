from fastapi import FastAPI, Body
from workspace.databaseconfig import DataBase
from workspace.roles import *
from typing import Annotated

#####################
app = FastAPI()     #
db = DataBase()     # 
#####################


@app.get('/family')
async def show_family():
    return {
        'family': db
    }

@app.put('/family/add_parent')
async def add_parent(parent: Annotated[
    Parent, 
    Body(..., example={
        'name': 'John',
        'role': 'Parent',
        'last_name': 'Doe',
        'password': 'securepassword'
    })
    ]):
    if parent.role != 'Parent':
        return {"message": "Invalid role"}
    db.add(parent)
    return {
        "message": "Parent added successfully",
        'family': db
            }

@app.put('/family/add_child')
async def add_child(child: Annotated[
    Children,
    Body(..., example={
        'name': 'Jane',
        'role': 'Child',
        'last_name': 'Doe',
        'password': 'securepassword'
    })
    ]):
    if child.role != 'Child':
        return {"message": "Invalid role"}
    db.add(child)
    return {
        "message": "Child added successfully",
        'family': db
    }

