from fastapi import FastAPI
from app.routers.register import router as register_router
from app.routers.login.login_customer import router as login_customer_router
from app.routers.login.forgot_password import router as forgot_password_router
from app.routers.login.reset_password import router as reset_password_router
from app.routers.login.login_collaborator import router as login_collaborator_router
from app.routers.collaborator_dash.dashboard_collaborator import router as dashboard_router
from app.routers.collaborator_dash.employees import router as employees_router
from app.routers.collaborator_dash.collaborators import router as collaborators_router
from app.routers.collaborator_dash.plans import router as plans_router
from app.routers.collaborator_dash.candidates import router as candidates_router



app = FastAPI()

# 🔹 Rotas de Autenticação
app.include_router(register_router, prefix="/api")
app.include_router(login_customer_router, prefix="/api")
app.include_router(forgot_password_router, prefix="/api")
app.include_router(reset_password_router, prefix="/api")
app.include_router(login_collaborator_router, prefix="/api")

# 🔹 Rotas do Dashboard do Colaborador
app.include_router(dashboard_router, prefix="/api/collaborator")  # Dashboard
app.include_router(employees_router, prefix="/api/dashboard")  # Updated prefix
app.include_router(collaborators_router, prefix="/api/dashboard")  # Changed this line
app.include_router(plans_router, prefix="/api/collaborator")
app.include_router(candidates_router, prefix="/api/collaborator")



@app.get("/")
def root():
    return {"message": "API funcionando"}