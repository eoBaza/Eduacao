from pydantic import BaseModel, EmailStr

# Criar o Usuario
class UsuarioCreate(BaseModel):
    id: int
    nome: str
    gmail: EmailStr
    tipo_usuario: str
    cnpj_cpf: str
    senha_hash: str

# Retorno da API para o banco
class UsuarioResponse(BaseModel):
    pass