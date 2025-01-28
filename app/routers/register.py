from fastapi import APIRouter, HTTPException
from app.models.customer import CustomerCreate
from app.services.customer_service import create_customer, get_street_from_cep, is_valid_password
from app.database import customers_collection

router = APIRouter()

@router.post("/register")
def register_customer(customer: CustomerCreate):
    # Verificar se o e-mail já existe
    existing_email = customers_collection.find_one({"email": customer.email})
    if existing_email:
        raise HTTPException(status_code=400, detail="E-mail já cadastrado")
    
    # Verificar se o telefone já existe
    existing_phone = customers_collection.find_one({"phone": customer.phone})
    if existing_phone:
        raise HTTPException(status_code=400, detail="Telefone já cadastrado")

    # Validar a senha
    if not is_valid_password(customer.password):
        raise HTTPException(
            status_code=400,
            detail="A senha deve conter pelo menos 4 letras, 2 números e 1 caractere especial"
        )

    # Buscar a rua automaticamente pelo CEP
    customer.street = get_street_from_cep(customer.cep)
    if not customer.street:
        raise HTTPException(status_code=400, detail="CEP inválido ou não encontrado")

    # Criar o cliente no banco
    new_customer = create_customer(customer.dict())
    return {"message": "Cliente registrado com sucesso", "id": str(new_customer)}

@router.get("/get-street/{cep}")
def get_street(cep: str):
    street = get_street_from_cep(cep)
    if not street:
        raise HTTPException(status_code=404, detail="CEP inválido ou não encontrado")
    return {"street": street}
