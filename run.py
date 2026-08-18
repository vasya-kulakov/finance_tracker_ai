from fastapi import FastAPI, Body, Path, HTTPException, status
from workspace.docs import Docs
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
        'family': db.base
    }

@app.put('/family/add_parent')
async def add_parent(parent: Annotated[
    Parent, 
    Body(..., example=Docs.parent_docs_json_format)
    ]):
    parent = parent.model_dump()
    parent['role'] = 'Parent'
    db.add(parent)
    return {
        "message": "Parent added successfully",
        'family': db.base
            }

@app.put('/family/add_child')
async def add_child(child: Annotated[
    Children,
    Body(..., example=Docs.child_docs_json_format)
    ]):
    child = child.model_dump()
    child['role'] = 'Child'
    child['capital'] = 0
    db.add(child)
    return {
        "message": "Child added successfully",
        'family': db.base
    }


@app.post('/family/{id_child}')
async def add_child_capital(
    id_child: Annotated[int, Path(..., title='Child id')], 
    token: Annotated[str, Body(..., title='Password - need to password for id parent, who`s be in children info')], 
    money: Annotated[int, Body(..., title='How much we get a child')]
    ):
    child = db.search(id_child)
    if 'Error' in child:
        if child['Error'] == 404:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail="Child id not found"
            )


    if db.check_validated_password(child['parent_id'], token):
        child['capital'] += money
        db.add(child)
        return {'msg': 'Capital was added succesfull', 'family': db.base}
    else:
        db.add(child)
        return {'msg': 'Error parent password'}

    