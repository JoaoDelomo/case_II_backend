from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.database import customers_collection
from app.services.customer_service import hash_password
from datetime import datetime

router = APIRouter()

class ResetPasswordRequest(BaseModel):
    identifier: str
    code: str
    new_password: str

@router.post("/reset-password")
def reset_password(request: ResetPasswordRequest):
    """
    Redefine a senha do cliente após validação do código de verificação.
    """
    customer = customers_collection.find_one({"$or": [{"email": request.identifier}, {"phone": request.identifier}]})

    if not customer or "verification_code" not in customer:
        raise HTTPException(status_code=400, detail="Código inválido ou expirado")

    if customer["verification_code"] != request.code:
        raise HTTPException(status_code=400, detail="Código incorreto")

    if datetime.utcnow() > customer["code_expiration"]:
        raise HTTPException(status_code=400, detail="Código expirado")

    # Atualiza a senha no banco de dados
    hashed_password = hash_password(request.new_password)
    customers_collection.update_one(
        {"_id": customer["_id"]},
        {"$set": {"hashed_password": hashed_password}, "$unset": {"verification_code": "", "code_expiration": ""}}
    )

    return {"message": "Senha redefinida com sucesso"}
