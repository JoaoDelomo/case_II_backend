from pydantic import BaseModel, EmailStr, Field
from fastapi import APIRouter, Depends, HTTPException
from app.database import customers_collection
from app.services.auth_service import get_current_customer

router = APIRouter()

class CustomerCreate(BaseModel):
    name: str
    email: EmailStr
    phone: str = Field(..., pattern=r'^\d{10,11}$')
    cpf: str
    password: str
    cep: str
    street: str | None = None
    number: str
    complement: str | None = None
    city: str
    state: str

class CustomerDB(CustomerCreate):
    hashed_password: str


@router.get("/customer", tags=["Customer"])
def get_customer_data(customer=Depends(get_current_customer)):
    """
    🔹 Retorna os dados do cliente autenticado
    """
    if not customer:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")

    # 🔹 Converte o `_id` de ObjectId para string
    customer["_id"] = str(customer["_id"])

    # 🔹 Remove a senha antes de retornar os dados
    customer.pop("hashed_password", None)

    print("📡 Dados do cliente retornados:", customer)  # <-- Log no backend

    return customer