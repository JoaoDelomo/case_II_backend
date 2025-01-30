import re
from app.database import collaborators_collection
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
    if len(password) < 7:
        return False

    letters = len(re.findall(r'[a-zA-Z]', password))
    digits = len(re.findall(r'\d', password))
    special_chars = len(re.findall(r'[!@#$%^&*(),.?":{}|<>\-_=+]', password))

    return letters >= 4 and digits >= 2 and special_chars >= 1

def create_collaborator(collaborator_data: dict):
    """
    Cria um colaborador no banco de dados. Somente o admin pode criar.
    """
    if not is_valid_password(collaborator_data["password"]):
        raise ValueError("A senha deve conter pelo menos 4 letras, 2 números e 1 caractere especial")
    
    # Gerar hash da senha antes de salvar
    collaborator_data["hashed_password"] = hash_password(collaborator_data.pop("password"))

    # Inserir no banco de dados
    result = collaborators_collection.insert_one(collaborator_data)
    return result.inserted_id

def authenticate_collaborator_by_email(email: str, password: str) -> dict | None:
    """
    Autentica o colaborador verificando e-mail e senha.
    Retorna o colaborador se autenticado, ou None caso contrário.
    """
    collaborator = collaborators_collection.find_one({"email": email})
    if not collaborator or not verify_password(password, collaborator["hashed_password"]):
        return None
    return collaborator

