from fastapi import APIRouter, Depends, HTTPException
from app.database import ps_collection  # Certifique-se de que a coleção existe
from app.services.auth_service import get_current_collaborator
from bson import ObjectId

router = APIRouter()

### 📌 1️⃣ ROTA - Listar todos os candidatos ###
@router.get("/candidates", tags=["Candidates"])
def get_candidates(collaborator=Depends(get_current_collaborator)):
    """
    Retorna todos os candidatos no processo seletivo.
    Apenas colaboradores autenticados podem acessar.
    """
    candidates = list(ps_collection.find({}, {"_id": 1, "vaga": 1, "nome": 1, "email": 1, "telefone": 1, "status_processo": 1}))

    for candidate in candidates:
        candidate["_id"] = str(candidate["_id"])  # Converte ObjectId para string

    return {"candidates": candidates}


### 📌 2️⃣ ROTA - Criar um novo candidato ###
@router.post("/candidates", tags=["Candidates"])
def create_candidate(candidate: dict, collaborator=Depends(get_current_collaborator)):
    """
    Cria um novo candidato.
    Campos obrigatórios: vaga, nome, email, telefone, status_processo.
    """
    required_fields = ["vaga", "nome", "email", "telefone", "status_processo"]
    
    if not all(field in candidate for field in required_fields):
        raise HTTPException(status_code=400, detail=f"Campos obrigatórios: {', '.join(required_fields)}")

    result = ps_collection.insert_one(candidate)
    return {"message": "Candidato criado com sucesso!", "id": str(result.inserted_id)}


### 📌 3️⃣ ROTA - Atualizar um candidato existente ###
@router.put("/candidates/{candidate_id}", tags=["Candidates"])
def update_candidate(candidate_id: str, update_data: dict, collaborator=Depends(get_current_collaborator)):
    """
    Atualiza os detalhes de um candidato existente pelo ID.
    """
    try:
        object_id = ObjectId(candidate_id)
    except:
        raise HTTPException(status_code=400, detail="ID inválido.")

    existing_candidate = ps_collection.find_one({"_id": object_id})
    if not existing_candidate:
        raise HTTPException(status_code=404, detail="Candidato não encontrado.")

    update_fields = {key: value for key, value in update_data.items() if value is not None}

    if not update_fields:
        raise HTTPException(status_code=400, detail="Nenhum dado para atualizar.")

    ps_collection.update_one({"_id": object_id}, {"$set": update_fields})
    return {"message": "Candidato atualizado com sucesso!"}


### 📌 4️⃣ ROTA - Deletar um candidato ###
@router.delete("/candidates/{candidate_id}", tags=["Candidates"])
def delete_candidate(candidate_id: str, collaborator=Depends(get_current_collaborator)):
    """
    Remove um candidato do processo seletivo pelo ID.
    """
    try:
        object_id = ObjectId(candidate_id)
    except:
        raise HTTPException(status_code=400, detail="ID inválido.")

    result = ps_collection.delete_one({"_id": object_id})

    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Candidato não encontrado.")

    return {"message": "Candidato removido com sucesso!"}
