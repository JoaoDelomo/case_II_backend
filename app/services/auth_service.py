from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from app.database import collaborators_collection, customers_collection  # Adicionando customers_collection
import os

SECRET_KEY = os.getenv("SECRET_KEY", "sua_secret_key_super_segura")
ALGORITHM = "HS256"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/login/customer")  # Alterando para o login do cliente

def get_current_collaborator(token: str = Depends(oauth2_scheme)):
    """
    Decodifica o token JWT e retorna os dados do colaborador autenticado.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")

        if email is None:
            raise HTTPException(status_code=401, detail="Token inválido")

        collaborator = collaborators_collection.find_one({"email": email})
        if not collaborator:
            raise HTTPException(status_code=401, detail="Usuário não encontrado")

        return collaborator
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido")

# 🔹 Função para validar o token do cliente (customer)
def get_current_customer(token: str = Depends(oauth2_scheme)):
    """
    Decodifica o token JWT e retorna os dados do cliente autenticado.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")

        if email is None:
            raise HTTPException(status_code=401, detail="Token inválido")

        customer = customers_collection.find_one({"email": email})
        if not customer:
            raise HTTPException(status_code=401, detail="Usuário não encontrado")

        return customer
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido")
