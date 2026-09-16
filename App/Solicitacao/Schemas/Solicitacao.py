from pydantic import BaseModel
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
    id_user_requerente: int 
    lista_itens: list[dict]
    quantidade_meninas: int 
    quantidade_meninos: int 
    status: SolicitacaoStatus = SolicitacaoStatus.CRIADO
    dt_criada: datetime