from pydantic import BaseModel, EmailStr
from enum import Enum

# Definir Enum com os valores permitidos pelo banco
class TipoUsuarioEnum(str, Enum):
    F = "F"
    J = "J"
    M = "M"

# Criar o Usuario
class UsuarioCreate(BaseModel):
    nome: str
    gmail: EmailStr
    tipo_usuario: TipoUsuarioEnum
    cnpj_cpf: str
    senha_hash: str

# Retorno da API para o banco
class UsuarioResponse(BaseModel):
    nome: str
    gmail: EmailStr
    tipo_usuario: TipoUsuarioEnum
    cnpj_cpf: str

# Login do Usario
class UsuarioLogin(BaseModel):
    gmail: EmailStr
    senha: str