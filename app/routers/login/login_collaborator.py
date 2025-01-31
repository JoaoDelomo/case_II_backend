from fastapi import APIRouter, HTTPException
from datetime import datetime, timedelta
from jose import JWTError, jwt
from pydantic import BaseModel
from app.services.collaborator_service import authenticate_collaborator

# Configurações do Token JWT
SECRET_KEY = "sua_secret_key_super_segura"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

router = APIRouter()

# Modelo para receber as credenciais de login
class LoginData(BaseModel):
    email: str
    cpf: str
    password: str


# Modelo para o token de resposta
class Token(BaseModel):
    access_token: str
    token_type: str

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    """Cria um token JWT com dados e expiração"""
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

@router.post("/login/collaborator", response_model=Token)
def login_collaborator(login_data: LoginData):
    print("🔍 Dados recebidos:", login_data.dict())  # ADICIONE ESSA LINHA PARA DEBUG
    """
    Autentica o colaborador por e-mail e CPF e retorna um token JWT.
    """
    collaborator = authenticate_collaborator(login_data.email, login_data.cpf, login_data.password)
    if not collaborator:
        raise HTTPException(status_code=401, detail="E-mail, CPF ou senha incorretos")
    
    # Gerar o token JWT
    access_token = create_access_token(data={"sub": collaborator["email"], "role": "collaborator"})
    return {"access_token": access_token, "token_type": "bearer"}

