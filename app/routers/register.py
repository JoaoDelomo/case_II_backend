from fastapi import APIRouter, HTTPException, Response
from app.models.customer import CustomerCreate
from app.services.customer_service import create_customer, is_valid_password
from app.database import customers_collection

router = APIRouter()

@router.options("/register")
def preflight_register():
    """
    Responde a requisições OPTIONS para o CORS.
    """
    return Response(headers={"Access-Control-Allow-Origin": "*",
                             "Access-Control-Allow-Methods": "POST, OPTIONS",
                             "Access-Control-Allow-Headers": "*"})


@router.post("/register")
def register_customer(customer: CustomerCreate):
    """
    Registra um novo cliente.
    """
    # 🔹 Verificar se o e-mail já existe
    if customers_collection.find_one({"email": customer.email}):
        raise HTTPException(status_code=400, detail="E-mail já cadastrado")

    # 🔹 Verificar se o telefone já existe
    if customers_collection.find_one({"phone": customer.phone}):
        raise HTTPException(status_code=400, detail="Telefone já cadastrado")

    # 🔹 Validar a senha
    if not is_valid_password(customer.password):
        raise HTTPException(
            status_code=400,
            detail="A senha deve conter pelo menos 4 letras, 2 números e 1 caractere especial"
        )

    # 🔹 Criar o cliente no banco
    new_customer = create_customer(customer.dict())
    return {"message": "Cliente registrado com sucesso", "id": str(new_customer)}
