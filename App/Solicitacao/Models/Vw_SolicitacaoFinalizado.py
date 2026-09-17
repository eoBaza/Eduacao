from sqlalchemy import String, DateTime, Integer
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import JSONB
from typing import Any, Dict, List
from datetime import datetime

#Arquivos
from Database.Database import Base

class Vw_SolicitacaoPendente(Base):
    __tablename__ = "vw_solicitacaofinalizada"
    __table_args__ = {"schema": "educacao"}

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    usuario_requerente: Mapped[str] = mapped_column(String, nullable=False)
    lista_itens: Mapped[List[Dict[str, Any]]] = mapped_column(JSONB, nullable=False)
    status: Mapped[str] = mapped_column(String, nullable=False)
    dt_criada: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, nullable=False)
    usuario_apoiador: Mapped[str] = mapped_column(String, nullable=False)
    local_entrega: Mapped[str] = mapped_column(String, nullable=False)
    cep: Mapped[str] = mapped_column(String, nullable=False)