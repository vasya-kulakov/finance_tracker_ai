from fastapi import FastAPI
from src.api import main_router
from src.db.init_db import init_db


app = FastAPI(title="Family Finance Tracker")
app.include_router(main_router)


@app.on_event("startup")
async def startup_event():
    await init_db()


@app.get('/')
async def welcome_to_finance_tracker():
    return {
        'msg': 'welcome to my finance tracker. '
        'This project is only backend part of app. For use API I will recommended use a /docs path',
        'main_page': 1,
        'version': 0.6
    }

