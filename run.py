from fastapi import FastAPI
from workspace.databaseconfig import DataBase
from workspace.roles import *

#####################
app = FastAPI()     #
db = DataBase()     # 
#####################


@app.get('/family')
async def show():
    return {
        'family': db
    }

@app.put('/family/add_parent')
async def add_parent(parent: Parent):
    if parent.role != 'Parent':
        return {"message": "Invalid role"}
    db.add(parent)
    return {
        "message": "Parent added successfully",
        'family': db
            }

@app.put('/family/add_child')
async def add_child(child: Children):
    if child.role != 'Child':
        return {"message": "Invalid role"}
    db.add(child)
    return {
        "message": "Child added successfully",
        'family': db
    }

