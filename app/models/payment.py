from fastapi import APIRouter, Depends, HTTPException
from app.database import customers_collection, plans_collection
from app.services.auth_service import get_current_customer
from bson import ObjectId
from pydantic import BaseModel

router = APIRouter()

class PaymentData(BaseModel):
    plan_id: str
    card_number: str
    cvv: str
    card_holder: str
    cpf: str

@router.post("/payment/subscribe", tags=["Payment"])
def process_payment(payment: PaymentData, customer=Depends(get_current_customer)):
    """
    🔹 Processa o pagamento e armazena os dados do cartão, caso ainda não existam.
    """
    
    existing_customer = customers_collection.find_one({"_id": ObjectId(customer["_id"])})

    if existing_customer and "active_plan" in existing_customer:
        raise HTTPException(status_code=400, detail="Você já possui um plano ativo.")

    plan = plans_collection.find_one({"_id": ObjectId(payment.plan_id)})
    if not plan:
        raise HTTPException(status_code=404, detail="Plano não encontrado")

    # 🔹 Verifica se já existem dados do cartão
    existing_payment_info = existing_customer.get("payment_info", {})

    customers_collection.update_one(
        {"_id": ObjectId(customer["_id"])},
        {"$set": {
            "active_plan": {
                "id": str(plan["_id"]),
                "nome": plan["nome"],
                "franquia_internet": plan.get("franquia_internet", "Não especificado"),
                "preco": plan["preco"]
            },
            "payment_info": {
                "card_number": payment.card_number if not existing_payment_info.get("card_number") else existing_payment_info["card_number"],
                "card_holder": payment.card_holder if not existing_payment_info.get("card_holder") else existing_payment_info["card_holder"],
                "cpf": payment.cpf if not existing_payment_info.get("cpf") else existing_payment_info["cpf"],
                "cvv": payment.cvv if not existing_payment_info.get("cvv") else existing_payment_info["cvv"]
            }
        }}
    )

    return {"message": "Plano assinado com sucesso!", "plan": str(plan["_id"])}

@router.get("/customer/payment-info", tags=["Payment"])
def get_payment_info(customer=Depends(get_current_customer)):  
    """
    🔹 Retorna os dados do cartão salvo para conferência.
    """
    customer_data = customers_collection.find_one({"_id": ObjectId(customer["_id"])}, {"payment_info": 1})

    if not customer_data or "payment_info" not in customer_data:
        return {"payment_info": None}  # 🔹 Retorna None se não houver dados

    return {"payment_info": customer_data["payment_info"]}


@router.post("/payment/cancel", tags=["Payment"])
def cancel_plan(customer=Depends(get_current_customer)):
    """
    🔹 Cancela o plano ativo do cliente autenticado.
    """

    # 🔹 Verifica se o cliente tem um plano ativo
    existing_customer = customers_collection.find_one({"_id": ObjectId(customer["_id"])})
    if not existing_customer or "active_plan" not in existing_customer:
        raise HTTPException(status_code=400, detail="Nenhum plano ativo encontrado para cancelamento.")

    # 🔹 Remove o plano ativo do cliente
    customers_collection.update_one(
        {"_id": ObjectId(customer["_id"])},
        {"$unset": {"active_plan": ""}}  # Remove o campo active_plan
    )

    return {"message": "Plano cancelado com sucesso!"}
