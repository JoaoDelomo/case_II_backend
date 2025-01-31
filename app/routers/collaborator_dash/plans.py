from fastapi import APIRouter, Depends, HTTPException
from app.database import plans_collection
from app.services.auth_service import get_current_collaborator  # 🔹 Proteção com autenticação
from bson import ObjectId

router = APIRouter()

### 📌 1️⃣ ROTA - Listar todos os planos (PÚBLICO) ###
@router.get("/plans", tags=["Plans"])
def get_plans():
    """
    Retorna todos os planos disponíveis.
    Essa rota é pública e pode ser acessada por qualquer usuário.
    """
    plans = list(plans_collection.find({}, {"_id": 1, "nome": 1, "preco": 1, "beneficios": 1}))

    for plan in plans:
        plan["_id"] = str(plan["_id"])  # Converte ObjectId para string

    return {"plans": plans}


### 📌 2️⃣ ROTA - Criar um novo plano (SOMENTE COLABORADORES) ###
@router.post("/plans", tags=["Plans"])
def create_plan(plan: dict, collaborator=Depends(get_current_collaborator)):  # 🔒 Proteção aqui!
    """
    Cria um novo plano.
    Somente colaboradores autenticados podem criar.
    """
    if "nome" not in plan or "preco" not in plan or "beneficios" not in plan:
        raise HTTPException(status_code=400, detail="Campos 'nome', 'preco' e 'beneficios' são obrigatórios.")

    result = plans_collection.insert_one(plan)
    return {"message": "Plano criado com sucesso!", "id": str(result.inserted_id)}


### 📌 3️⃣ ROTA - Atualizar um plano existente (SOMENTE COLABORADORES) ###
@router.put("/plans/{plan_id}", tags=["Plans"])
def update_plan(plan_id: str, update_data: dict, collaborator=Depends(get_current_collaborator)):  # 🔒 Proteção aqui!
    """
    Atualiza os detalhes de um plano existente pelo ID.
    Somente colaboradores autenticados podem editar planos.
    """
    try:
        object_id = ObjectId(plan_id)
    except:
        raise HTTPException(status_code=400, detail="ID inválido.")

    existing_plan = plans_collection.find_one({"_id": object_id})
    if not existing_plan:
        raise HTTPException(status_code=404, detail="Plano não encontrado.")

    update_fields = {key: value for key, value in update_data.items() if value is not None}

    if not update_fields:
        raise HTTPException(status_code=400, detail="Nenhum dado para atualizar.")

    plans_collection.update_one({"_id": object_id}, {"$set": update_fields})
    return {"message": "Plano atualizado com sucesso!"}


### 📌 4️⃣ ROTA - Deletar um plano (SOMENTE COLABORADORES) ###
@router.delete("/plans/{plan_id}", tags=["Plans"])
def delete_plan(plan_id: str, collaborator=Depends(get_current_collaborator)):  # 🔒 Proteção aqui!
    """
    Remove um plano pelo ID.
    Somente colaboradores autenticados podem excluir.
    """
    try:
        object_id = ObjectId(plan_id)
    except:
        raise HTTPException(status_code=400, detail="ID inválido.")

    result = plans_collection.delete_one({"_id": object_id})

    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Plano não encontrado.")

    return {"message": "Plano removido com sucesso!"}
