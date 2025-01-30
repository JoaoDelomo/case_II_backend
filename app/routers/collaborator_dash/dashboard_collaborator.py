from fastapi import APIRouter, Depends, HTTPException
from app.database import feedbacks_collection, customers_collection, funcionarios_collection, collaborators_collection
from app.services.auth_service import get_current_collaborator
from app.services.collaborator_service import hash_password
from bson import ObjectId

router = APIRouter()

### 📌 1️⃣ ROTA - Resumo dos feedbacks ###
@router.get("/dashboard/feedbacks", tags=["Dashboard"])
def get_feedbacks_dashboard(collaborator=Depends(get_current_collaborator)):
    feedbacks = list(feedbacks_collection.find({}, {"_id": 0, "SatisfacaoPosAtendimento": 1}))
    feedback_summary = {}
    
    for fb in feedbacks:
        nota = fb.get("SatisfacaoPosAtendimento", 0)
        feedback_summary[nota] = feedback_summary.get(nota, 0) + 1

    return {"feedback_summary": feedback_summary}

### 📌 2️⃣ ROTA - Listar clientes ###
@router.get("/dashboard/customers", tags=["Dashboard"])
def get_customers_dashboard(collaborator=Depends(get_current_collaborator)):
    customers = list(customers_collection.find({}, {"_id": 0, "name": 1, "city": 1}))
    return {"customers": customers}




