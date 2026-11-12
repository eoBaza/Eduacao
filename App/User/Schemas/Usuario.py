from pydantic import BaseModel, EmailStr
from enum import Enum

# Tipos de usuário retornados pela VIEW
class TipoUsuarioEnum(str, Enum):
    JURIDICO = "Juridico"
    FISICO = "Fisico"
    MOTORISTA = "Motorista"

# Criar o Usuario
class UsuarioCreate(BaseModel):
    nome: str
    gmail: EmailStr
    id_tipo_usuario: int
    cnpj_cpf: str
    senha: str
    id_endereco: int | None = None

# Retorno da API para o banco
class UsuarioResponse(BaseModel):
    id: int
    nome: str
    gmail: EmailStr | None
    id_tipo_usuario: int
    cnpj_cpf: str
    id_endereco: int | None

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

# Info dashbord Usuario
class Vw_UsuarioInfoResponse(BaseModel):
    id_usuario: int
    nome: str
    gmail: str | None
    tipo_usuario: TipoUsuarioEnum
    cnpj_cpf: str
    cep: str | None
    endereco: str | None
    numero: str | None
    complemento: str | None

class MessageResponse(BaseModel):
    message: str
