# Conta Corrente bancária
#  quero acompanha as entradas e saidas da minha conta corrente
from fastapi import FastAPI
import uvicorn
from pydantic import BaseModel, Field 


app = FastAPI(title="Banco Simples")

db = {
    'joao':0,
    'lucas':0,
    'maria':7540,
    'pedro':1010
}


class ClienteMov(BaseModel):
    nome:str = Field(...,description="Nome do cliente")
    valor:int = Field(..., gt=0,description="Valor da operação")


# criar uma classe para o banco

        

# add cliente

# add deposito

# add sacar

# add acompanhar saldo

# add conta corrente

@app.get('/')
def read_root():
    return {"Hello": "World"}   


@app.get('/saldo/{nome}')
def get_cliente(nome:str):
    if nome not in db:
        return {'error':'cliente não encontrado'}
    return {
        'nome':f'{nome}',
        'saldo do Clientes':f'R$ {db[nome] / 100}',  
    }

@app.post('/saque')
def saque(cliente:ClienteMov):
    if cliente.nome not in db:
        return {'error':'cliente não encontrado'}
    if cliente.valor > db[cliente.nome]:
        return {'error':'saldo insuficiente'}
    db[cliente.nome] -= cliente.valor
    return {'nome':cliente.nome,'saldo':db[cliente.nome]}

@app.post('/deposito')
def deposito(cliente:ClienteMov):
    if cliente.nome not in db:
        return {'error':'cliente não encontrado'}
    db[cliente.nome] += cliente.valor
    return {'nome':f'Deposito realizado por : {cliente.nome} depositado R$ {cliente.valor / 100}', 'saldo':f'R$ {db[cliente.nome] / 100}'}


if __name__ == '__main__':
    uvicorn.run('fast:app', host='0.0.0.0', port=8000, reload=True)