from fastapi import FastAPI
from app.routers.register import router

app = FastAPI()

app.include_router(router, prefix="/api")

@app.get("/")
def root():
    return {"message": "API funcionando"}
