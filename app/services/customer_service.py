import re
import requests
from app.database import costumers_collection
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    """Gera o hash de uma senha"""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifica se uma senha corresponde ao hash"""
    return pwd_context.verify(plain_password, hashed_password)

def is_valid_password(password: str) -> bool:
    """
    Verifica se a senha atende aos critérios:
    - Pelo menos 4 letras (a-z ou A-Z)
    - Pelo menos 2 números (0-9)
    - Pelo menos 1 caractere especial (!@#$%^&*()-+_=,<>?/ etc.)
    """
    if len(password) < 7:  # Tamanho mínimo sugerido (opcional)
        return False

    # Verifica letras
    letters = len(re.findall(r'[a-zA-Z]', password))
    # Verifica números
    digits = len(re.findall(r'\d', password))
    # Verifica caracteres especiais
    special_chars = len(re.findall(r'[!@#$%^&*(),.?":{}|<>\-_=+]', password))

    # Retorna True se todos os critérios forem atendidos
    return letters >= 4 and digits >= 2 and special_chars >= 1

def get_street_from_cep(cep: str) -> str | None:
    """Busca a rua automaticamente pelo CEP usando a API ViaCEP"""
    url = f"https://viacep.com.br/ws/{cep}/json/"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data.get("logradouro")  # Retorna a rua
    return None

def create_customer(customer_data: dict):
    """
    Cria o cliente no banco de dados após validações
    """
    # Valida a senha
    if not is_valid_password(customer_data["password"]):
        raise ValueError("A senha deve conter pelo menos 4 letras, 2 números e 1 caractere especial")
    
    # Gera o hash da senha
    customer_data["hashed_password"] = hash_password(customer_data.pop("password"))

    # Valida e busca a rua a partir do CEP
    customer_data["street"] = get_street_from_cep(customer_data.get("cep"))
    if not customer_data["street"]:
        raise ValueError("CEP inválido ou não encontrado")

    # Insere no banco de dados
    result = costumers_collection.insert_one(customer_data)
    return result.inserted_id  # Retorna o ID do documento criado
