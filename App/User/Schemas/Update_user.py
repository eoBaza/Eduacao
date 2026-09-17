from pydantic import BaseModel, ConfigDict

class UsuarioUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    # usuario
    nome: str | None = None
    gmail: str | None = None

    # endereco
    endereco: str | None = None
    complemento: str | None = None
    cep: str | None = None
    numero: str | None = None
