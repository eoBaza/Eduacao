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
    senha: str
    id_endereco: int

# Retorno da API para o banco
class UsuarioResponse(BaseModel):
    id: int
    nome: str
    gmail: EmailStr
    tipo_usuario: TipoUsuarioEnum
    cnpj_cpf: str
    id_endereco: int
    class Config:
        from_attributes = True

# Schema de Requisicao do Login (Input do Post /Login)
class UsuarioLogin(BaseModel):
    gmail: EmailStr
    senha: str

# Resposta de Login quando User conseguir logar
class LoginResponse(BaseModel):
    message: str
    Session_Code: str

# Reset senha do usuario
class ResetSenha(BaseModel):
    gmail: EmailStr
    senha: str
    confirma_senha: str

class ResetSenhaResponse(BaseModel):
    message: str