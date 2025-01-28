from fastapi import FastAPI
from app.routers.register import router
from app.routers.login.login_customer import router as login_customer_router

app = FastAPI()

app.include_router(router, prefix="/api")

app.include_router(login_customer_router, prefix="/api")


@app.get("/")
def root():
    return {"message": "API funcionando"}
