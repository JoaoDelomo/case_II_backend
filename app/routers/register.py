from fastapi import APIRouter, HTTPException
from app.models.customer import CustomerCreate
from app.services.customer_service import create_customer, get_street_from_cep
from app.database import costumers_collection

router = APIRouter()

@router.post("/register")
def register_customer(customer: CustomerCreate):
    existing_customer = costumers_collection.find_one({"email": customer.email})
    if existing_customer:
        raise HTTPException(status_code=400, detail="E-mail já cadastrado")
    
    # Buscar a rua automaticamente pelo CEP
    street = get_street_from_cep(customer.cep)
    if not street:
        raise HTTPException(status_code=400, detail="CEP inválido ou não encontrado")
    
    customer.street = street  # Adiciona a rua ao objeto `customer`

    # Criar o cliente no banco de dados
    new_customer = create_customer(customer.dict())
    return {"message": "Cliente registrado com sucesso", "id": str(new_customer)}

@router.get("/get-street/{cep}")
def get_street(cep: str):
    street = get_street_from_cep(cep)
    if not street:
        raise HTTPException(status_code=404, detail="CEP inválido ou não encontrado")
    return {"street": street}
