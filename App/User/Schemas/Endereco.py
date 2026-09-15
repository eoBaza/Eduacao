from pydantic import BaseModel

class EnderecoCreate(BaseModel):
    endereco: str
    cep: str
    numero: str
    complemento: str
    id_regiao: int

#class EnderecoResponse(BaseModel)