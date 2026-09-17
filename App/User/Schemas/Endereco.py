from pydantic import BaseModel

class EnderecoCreate(BaseModel):
    endereco: str
    cep: str
    numero: str
    complemento: str
    id_regiao: int

class EnderecoUpdate(BaseModel):
    cep: str | None = None
    endereco: str | None = None
    complemento: str | None = None
    numero: str | None = None