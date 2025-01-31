from fastapi import APIRouter, HTTPException
from datetime import datetime, timedelta
from jose import JWTError, jwt
from pydantic import BaseModel
from app.services.customer_service import authenticate_customer_by_email_or_phone

# Configurações do Token JWT
SECRET_KEY = "sua_secret_key_super_segura"  # Altere para algo seguro e único
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

router = APIRouter()

# Modelo para receber as credenciais de login
class LoginData(BaseModel):
    identifier: str  # Pode ser e-mail ou telefone
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

@router.post("/login/customer", response_model=Token)
def login_customer(login_data: LoginData):
    """
    Autentica o cliente por e-mail ou telefone e retorna um token JWT.
    """
    # Autenticar o cliente com e-mail ou telefone e senha
    customer = authenticate_customer_by_email_or_phone(login_data.identifier, login_data.password)
    if not customer:
        raise HTTPException(status_code=401, detail="E-mail/telefone ou senha incorretos")
    
    # Gerar o token JWT
    access_token = create_access_token(data={"sub": customer["email"]})
    return {"access_token": access_token, "token_type": "bearer"}
