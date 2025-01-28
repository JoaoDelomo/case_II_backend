from pydantic import BaseModel, EmailStr

class CustomerCreate(BaseModel):
    name: str
    email: EmailStr
    cpf: str
    password: str
    cep: str
    street: str | None = None  # Campo preenchido automaticamente
    number: str
    complement: str | None = None
    city: str
    state: str

class CustomerDB(CustomerCreate):
    hashed_password: str
