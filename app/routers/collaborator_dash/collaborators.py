from fastapi import APIRouter, HTTPException, Depends
from app.database import collaborators_collection
from app.services.auth_service import get_current_collaborator
from pydantic import BaseModel
from passlib.context import CryptContext
from app.services.collaborator_service import hash_password
from bson import ObjectId

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Modelo de colaborador
class CollaboratorCreate(BaseModel):
    name: str
    email: str
    password: str

class CollaboratorUpdate(BaseModel):
    name: str | None = None
    email: str | None = None
    password: str | None = None

### 📌 Listar colaboradores ###
@router.get("/collaborators", tags=["Dashboard"])
def list_collaborators(current_collaborator=Depends(get_current_collaborator)):
    """
    Lista todos os colaboradores
    """
    collaborators = list(collaborators_collection.find({}, {"hashed_password": 0}))
    
    # Convert ObjectId to string for JSON serialization
    for collab in collaborators:
        collab["_id"] = str(collab["_id"])
    
    return collaborators

### 📌 Criar colaborador ###
@router.post("/collaborators", tags=["Dashboard"])
def create_collaborator(collaborator_data: dict, current_collaborator=Depends(get_current_collaborator)):
    """
    Cria um novo colaborador
    """
    if "name" not in collaborator_data or "email" not in collaborator_data or "password" not in collaborator_data:
        raise HTTPException(status_code=400, detail="Campos 'name', 'email' e 'password' são obrigatórios.")

    # Verificar se email já existe
    existing_collaborator = collaborators_collection.find_one({"email": collaborator_data["email"]})
    if existing_collaborator:
        raise HTTPException(status_code=400, detail="Email já cadastrado")

    # Preparar dados para inserção
    new_collaborator = {
        "name": collaborator_data["name"],
        "email": collaborator_data["email"],
        "hashed_password": hash_password(collaborator_data["password"])
    }

    result = collaborators_collection.insert_one(new_collaborator)
    return {"message": "Novo colaborador criado com sucesso!", "id": str(result.inserted_id)}

### 📌 Obter colaborador específico ###
@router.get("/collaborators/{collaborator_id}", tags=["Dashboard"])
def get_collaborator(collaborator_id: str, current_collaborator=Depends(get_current_collaborator)):
    """
    Obtém um colaborador específico pelo ID
    """
    try:
        object_id = ObjectId(collaborator_id)
    except:
        raise HTTPException(status_code=400, detail="ID inválido")

    collaborator = collaborators_collection.find_one({"_id": object_id}, {"hashed_password": 0})
    
    if not collaborator:
        raise HTTPException(status_code=404, detail="Colaborador não encontrado")
    
    # Check if the user is trying to access their own information
    if str(current_collaborator["_id"]) != collaborator_id:
        raise HTTPException(status_code=403, detail="Acesso não autorizado")
    
    collaborator["_id"] = str(collaborator["_id"])
    return collaborator

### 📌 Atualizar colaborador ###
@router.put("/collaborators/{collaborator_id}", tags=["Dashboard"])
def update_collaborator(
    collaborator_id: str, 
    collaborator_update: dict,
    current_collaborator=Depends(get_current_collaborator)
):
    """
    Atualiza um colaborador específico
    """
    try:
        object_id = ObjectId(collaborator_id)
    except:
        raise HTTPException(status_code=400, detail="ID inválido")

    # Verificar se o colaborador existe
    existing_collaborator = collaborators_collection.find_one({"_id": object_id})
    if not existing_collaborator:
        raise HTTPException(status_code=404, detail="Colaborador não encontrado")

    # Check if the user is trying to update their own information
    if str(current_collaborator["_id"]) != collaborator_id:
        raise HTTPException(status_code=403, detail="Acesso não autorizado")

    # Preparar dados para atualização
    update_data = {}
    for field, value in collaborator_update.items():
        if value is not None:
            if field == "password":
                update_data["hashed_password"] = hash_password(value)
            elif field in ["name", "email"]:
                update_data[field] = value

    if not update_data:
        raise HTTPException(status_code=400, detail="Nenhum dado para atualizar")

    # Se estiver atualizando o email, verificar se já existe
    if "email" in update_data:
        email_exists = collaborators_collection.find_one({
            "_id": {"$ne": object_id},
            "email": update_data["email"]
        })
        if email_exists:
            raise HTTPException(status_code=400, detail="Email já cadastrado")

    collaborators_collection.update_one(
        {"_id": object_id},
        {"$set": update_data}
    )

    return {"message": "Colaborador atualizado com sucesso"}

### 📌 Deletar colaborador ###
@router.delete("/collaborators/{collaborator_id}", tags=["Dashboard"])
def delete_collaborator(collaborator_id: str, current_collaborator=Depends(get_current_collaborator)):
    """
    Permite que qualquer colaborador remova outro colaborador.
    """
    try:
        object_id = ObjectId(collaborator_id)  # Converte o ID para ObjectId do MongoDB
    except:
        raise HTTPException(status_code=400, detail="ID inválido")

    # Verifica se o colaborador existe antes de deletar
    existing_collaborator = collaborators_collection.find_one({"_id": object_id})
    if not existing_collaborator:
        raise HTTPException(status_code=404, detail="Colaborador não encontrado")

    # Excluir o colaborador
    result = collaborators_collection.delete_one({"_id": object_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Erro ao excluir colaborador")

    return {"message": "Colaborador removido com sucesso"}
