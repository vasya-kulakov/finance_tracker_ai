from fastapi import FastAPI
from databaseconfig import DataBase
app = FastAPI()

db = DataBase()


@app.get("/")
def read_root():
    return {"message": "Hello, World!"}


@app.get('/list')
def show():
    return db 

@app.put('/list')
def add_element(data: dict):
    el = data['element']
    db.add(el)
    return db

@app.delete('/list')
def delete_el(data: dict):
    el = data['element']
    db.delete(el)
    return db


