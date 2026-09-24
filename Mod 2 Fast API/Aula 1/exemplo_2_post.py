"""
Conta corrente bancária
Gerenciar saque e depositos de clientes
"""
from fastapi import FastAPI
from pydantic import BaseModel, Field
import uvicorn

# Inicializa a aplicação FastAPI
app = FastAPI(
    title="Conta Corrente Bancária",
    description="Gerenciar saque e depositos de clientes",
    version="0.1.0"
)

# Adicionar clientes, simulação de um banco de dados
db_clientes = {
    "123": {"nome": "João", "saldo": 1000.0},
    "456": {"nome": "Maria", "saldo": 2000.0},
}

# Criar uma classe para as movimentações (saques e depósitos) OBS: Usar Pydantic para validação de dados
class Movimentacao(BaseModel):
    cliente_id: str = Field(..., min_length=3, description="ID do cliente")
    cliente_nome: str = Field(..., min_length=3, description="Nome do cliente")
    valor: float = Field(..., gt=0, description="Valor da movimentação")
    tipo: str = Field(..., description="Tipo da movimentação (saque ou deposito)")


# Criar um  enpoint HOME (raiz)
@app.get("/")
async def read_root():
    return {"message": "Bem-vindo à Conta Corrente Bancária"}


# Criar um endpoint para consultar o saldo do cliente
@app.post("/saldo")
async def saldo(cliente: int):
    cliente_id = str(cliente)
    if cliente_id in db_clientes:
        return {"cliente": db_clientes[cliente_id]["nome"], "saldo": db_clientes[cliente_id]["saldo"]}
    else:
        return {"error": "Cliente não encontrado"}


# Criar um endpoint para realizar saques
@app.post("/saque")
async def saque(movimentacao: Movimentacao):
    db_clientes[movimentacao.cliente_id]["saldo"] -= movimentacao.valor
    return {"message": f"Saque de R${movimentacao.valor} realizado com sucesso para o cliente {movimentacao.cliente_nome}. Novo saldo: R${db_clientes[movimentacao.cliente_id]['saldo']}"}


# Criar um endpoint para realizar depósitos
@app.post("/deposito")
async def deposito(movimentacao: Movimentacao):
    db_clientes[movimentacao.cliente_id]["saldo"] += movimentacao.valor
    return {"message": f"Depósito de R${movimentacao.valor} realizado com sucesso para o cliente {movimentacao.cliente_nome}. Novo saldo: R${db_clientes[movimentacao.cliente_id]['saldo']}"}


if __name__ == "__main__":
    uvicorn.run("exemplo_2_post:app", host="0.0.0.0", port=8000, reload=True)