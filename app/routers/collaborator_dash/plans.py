from fastapi import APIRouter, Depends, HTTPException
from app.database import plans_collection  # Certifique-se que essa coleção existe no banco
from app.services.auth_service import get_current_collaborator
from bson import ObjectId

router = APIRouter()

### 📌 1️⃣ ROTA - Listar todos os planos ###
@router.get("/plans", tags=["Plans"])
def get_plans(collaborator=Depends(get_current_collaborator)):
    """
    Retorna todos os planos disponíveis.
    Apenas colaboradores autenticados podem acessar.
    """
    plans = list(plans_collection.find({}, {"_id": 1, "nome": 1, "preco": 1, "beneficios": 1}))

    for plan in plans:
        plan["_id"] = str(plan["_id"])  # Converte ObjectId para string

    return {"plans": plans}


### 📌 2️⃣ ROTA - Criar um novo plano ###
@router.post("/plans", tags=["Plans"])
def create_plan(plan: dict, collaborator=Depends(get_current_collaborator)):
    """
    Cria um novo plano.
    Campos obrigatórios: nome, preco, beneficios (lista).
    """
    if "nome" not in plan or "preco" not in plan or "beneficios" not in plan:
        raise HTTPException(status_code=400, detail="Campos 'nome', 'preco' e 'beneficios' são obrigatórios.")

    result = plans_collection.insert_one(plan)
    return {"message": "Plano criado com sucesso!", "id": str(result.inserted_id)}


### 📌 3️⃣ ROTA - Atualizar um plano existente ###
@router.put("/plans/{plan_id}", tags=["Plans"])
def update_plan(plan_id: str, update_data: dict, collaborator=Depends(get_current_collaborator)):
    """
    Atualiza os detalhes de um plano existente pelo ID.
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


### 📌 4️⃣ ROTA - Deletar um plano ###
@router.delete("/plans/{plan_id}", tags=["Plans"])
def delete_plan(plan_id: str, collaborator=Depends(get_current_collaborator)):
    print(f"🔹 Colaborador autenticado: {collaborator}")  # 🟢 Teste para ver se está autenticado

    try:
        object_id = ObjectId(plan_id)
    except:
        raise HTTPException(status_code=400, detail="ID inválido.")

    result = plans_collection.delete_one({"_id": object_id})

    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Plano não encontrado.")

    return {"message": "Plano removido com sucesso!"}


