from pydantic import BaseModel, ConfigDict
from datetime import datetime
from enum import Enum

class SolicitacaoStatus(str, Enum):
    CRIADO = "Criado Por Requerente"
    APOIADOR_JUNTO = "Apoiador se juntou a acao"
    PREPARANDO = "Preparando"
    FINALIZADO = "Finalizado"

class SolicitacaoReponse(BaseModel):
    id: int
    id_user_requerente: int
    lista_itens: list
    quantidade_meninas: int 
    quantidade_meninos: int
    id_user_apoiador: int | None = None
    status: SolicitacaoStatus
    dt_criada: datetime
    dt_finalizada: datetime | None = None
    
    
class SolicitacaoCreate(BaseModel):
    lista_itens: list[dict]
    quantidade_meninas: int 
    quantidade_meninos: int 
    status: SolicitacaoStatus = SolicitacaoStatus.CRIADO
    dt_criada: datetime

class SolicitacaoUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    lista_itens: list[dict] | None = None
    quantidade_meninas: int | None = None
    quantidade_meninos: int | None = None


class Vw_SolicitacaoPendenteResponse(BaseModel):
    id: int
    usuario_requerente: str
    lista_itens: str
    status: str
    dt_criada: str
    usuario_apoiador:str
    local_entrega: str
    cep: str
    
class Vw_SolicitacaoFinalizadaResponse(BaseModel):
    id: int
    usuario_requerente: str
    lista_itens: str
    status: str
    dt_criada: str
    usuario_apoiador:str
    local_entrega: str
    cep: str