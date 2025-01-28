from fastapi import FastAPI
from app.routers.register import router as register_router
from app.routers.login.login_customer import router as login_customer_router
from app.routers.login.forgot_password import router as forgot_password_router
from app.routers.login.reset_password import router as reset_password_router

app = FastAPI()

app.include_router(register_router, prefix="/api")
app.include_router(login_customer_router, prefix="/api")
app.include_router(forgot_password_router, prefix="/api")  # Certifique-se desse include
app.include_router(reset_password_router, prefix="/api")

@app.get("/")
def root():
    return {"message": "API funcionando"}
