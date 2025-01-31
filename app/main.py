from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
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
from app.models.payment import router as payment_router
from app.models.customer import router as customer_router

app = FastAPI()

# 🔹 Middleware CORS corretamente configurado
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # 🔹 Permite o front do React (Vite)
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],  # 🔹 Permite esses métodos
    allow_headers=["*"],  # 🔹 Permite todos os headers
)

# 🔹 Registrar as rotas corretamente
app.include_router(register_router, prefix="/api")
app.include_router(login_customer_router, prefix="/api")
app.include_router(forgot_password_router, prefix="/api")
app.include_router(reset_password_router, prefix="/api")
app.include_router(login_collaborator_router, prefix="/api")
app.include_router(dashboard_router, prefix="/api/collaborator")
app.include_router(employees_router, prefix="/api/dashboard")
app.include_router(collaborators_router, prefix="/api/dashboard")
app.include_router(candidates_router, prefix="/api/collaborator")
app.include_router(plans_router, prefix="/api")
app.include_router(payment_router, prefix="/api")
app.include_router(customer_router, prefix="/api")
