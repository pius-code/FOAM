from fastapi import FastAPI
from src.api.routes import api_router


app = FastAPI()


@app.get("/")
def welcome():
    return "welcome to FOAM"


app.include_router(api_router)
