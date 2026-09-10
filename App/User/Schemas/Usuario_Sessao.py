from pydantic import BaseModel
from datetime import datetime

# Criar Sessao do Usuario
class UsuarioSessaoCreate(BaseModel):
    id_usuario: int
    ativo: bool
    dt_expira: datetime
    sessao_code: str
    dt_criada: datetime

class UsuarioSessaoResponse(BaseModel):
    id_usuario: int
    ativo: bool
    sessao_code: bool
    dt_expirado: datetime
