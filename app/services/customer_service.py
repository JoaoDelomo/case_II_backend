import requests
from app.database import costumers_collection
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_street_from_cep(cep: str) -> str | None:
    """Busca a rua automaticamente pelo CEP usando a API ViaCEP"""
    url = f"https://viacep.com.br/ws/{cep}/json/"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data.get("logradouro")  # Retorna a rua
    return None

def create_customer(customer_data: dict):
    """Cria o cliente no banco de dados"""
    customer_data["hashed_password"] = hash_password(customer_data.pop("password"))
    result = costumers_collection.insert_one(customer_data)
    return result.inserted_id  # Retorna o ID do documento criado
