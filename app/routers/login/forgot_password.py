from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from random import randint
from datetime import datetime, timedelta
from app.services.email_service import send_email
from app.database import customers_collection

router = APIRouter()

class ForgotPasswordRequest(BaseModel):
    identifier: str

@router.post("/forgot-password")
def forgot_password(request: ForgotPasswordRequest):
    customer = customers_collection.find_one({"$or": [{"email": request.identifier}, {"phone": request.identifier}]})
    if not customer:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")

    # Gerar o código de verificação
    verification_code = str(randint(100000, 999999))  # Código de 6 dígitos
    expiration = datetime.utcnow() + timedelta(minutes=15)

    # Salvar o código e o tempo de expiração no banco
    customers_collection.update_one(
        {"_id": customer["_id"]},
        {"$set": {"verification_code": verification_code, "code_expiration": expiration}}
    )

    # Enviar o código por e-mail
    email_body = f"""
    Olá, {customer['name']}!
    Use o código abaixo para redefinir sua senha. Ele é válido por 15 minutos:

    Código: {verification_code}

    Caso não tenha solicitado, ignore esta mensagem.
    """
    send_email(customer["email"], "Código de Verificação", email_body)

    return {"message": "Código enviado por e-mail"}

class VerifyCodeRequest(BaseModel):
    identifier: str  # Email ou telefone
    code: str  # Código digitado pelo usuário

@router.post("/verify-code")
def verify_code(request: VerifyCodeRequest):
    """
    Verifica se o código de redefinição é válido e ainda não expirou.
    """
    customer = customers_collection.find_one({"$or": [{"email": request.identifier}, {"phone": request.identifier}]})

    if not customer or "verification_code" not in customer:
        raise HTTPException(status_code=400, detail="Código inválido ou expirado")

    if customer["verification_code"] != request.code:
        raise HTTPException(status_code=400, detail="Código incorreto")

    if datetime.utcnow() > customer["code_expiration"]:
        raise HTTPException(status_code=400, detail="Código expirado")

    return {"message": "Código válido"}
