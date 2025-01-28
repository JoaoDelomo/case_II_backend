from pydantic import BaseModel, EmailStr

class CustomerCreate(BaseModel):
    name: str
    email: EmailStr
    cpf: str
    password: str
    cep: str
    street: str | None = None
    number: str
    complement: str | None = None
    city: str
    state: str
    card_last_digits: str | None = None  # Últimos 4 dígitos
    card_holder_name: str | None = None  # Nome do titular
    card_expiry_date: str | None = None  # Data de expiração (MM/YY)
    card_cvv: str | None = None          # CVV criptografado

class CustomerDB(CustomerCreate):
    hashed_password: str
