from fastapi import APIRouter, HTTPException, Depends
from app.database import funcionarios_collection
from app.services.auth_service import get_current_collaborator
from pydantic import BaseModel
from bson import ObjectId

router = APIRouter()

# Modelo de funcionário
class Employee(BaseModel):
    Funcionario: str
    Salario: float

### 📌 3️⃣ ROTA - Listar funcionários ###
@router.get("/dashboard/employees", tags=["Dashboard"])
def get_employees_dashboard(collaborator=Depends(get_current_collaborator)):
    employees = list(funcionarios_collection.find({}, {"_id": 0, "Funcionario": 1, "Salario": 1}))
    return {"employees": employees}

### 📌 4️⃣ CRUD - Criar funcionário (Sem Pydantic) ###
@router.post("/employees", tags=["Dashboard"])
def create_employee(employee: dict, collaborator=Depends(get_current_collaborator)):
    """
    Adiciona um novo funcionário à base de dados.
    """
    if "Funcionario" not in employee or "Salario" not in employee:
        raise HTTPException(status_code=400, detail="Campos 'Funcionario' e 'Salario' são obrigatórios.")

    result = funcionarios_collection.insert_one(employee)
    return {"message": "Funcionário criado!", "id": str(result.inserted_id)}

### 📌 5️⃣ CRUD - Atualizar funcionário ###
@router.put("/employees/{employee_id}", tags=["Dashboard"])
def update_employee(employee_id: str, employee: dict, collaborator=Depends(get_current_collaborator)):
    """
    Atualiza os dados de um funcionário pelo ID no MongoDB.
    """
    try:
        object_id = ObjectId(employee_id)  # ✅ Convertendo corretamente para ObjectId
    except Exception:
        raise HTTPException(status_code=400, detail="ID inválido, formato incorreto.")

    # 🔹 Verifica se o funcionário existe antes de atualizar
    existing_employee = funcionarios_collection.find_one({"_id": object_id})
    if not existing_employee:
        raise HTTPException(status_code=404, detail="Funcionário não encontrado no banco.")

    update_data = {key: value for key, value in employee.items() if value is not None}

    if not update_data:
        raise HTTPException(status_code=400, detail="Nenhum dado para atualizar.")

    # 🔹 Atualiza apenas os campos enviados no JSON
    funcionarios_collection.update_one({"_id": object_id}, {"$set": update_data})

    return {"message": "Funcionário atualizado com sucesso!"}

### 📌 6️⃣ CRUD - Excluir funcionário ###
@router.delete("/employees/{employee_id}", tags=["Dashboard"])
def delete_employee(employee_id: str, collaborator=Depends(get_current_collaborator)):
    try:
        query = {"_id": ObjectId(employee_id)}
    except Exception:
        raise HTTPException(status_code=400, detail="ID inválido")

    result = funcionarios_collection.delete_one(query)

    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Funcionário não encontrado")

    return {"message": "Funcionário removido!"}

