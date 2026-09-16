from sqlalchemy import String, Integer, ForeignKey, DateTime, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import JSONB
from typing import Any, Dict, List,Optional
from datetime import datetime

#Arquivos
from Database.Database import Base
from Solicitacao.Schemas.Solicitacao import SolicitacaoStatus

class Solicitacao(Base):
    __tablename__ = "solicitacao"
    __table_args__ = {"schema": "educacao", "extend_existing": True}

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    id_user_requerente: Mapped[int] = mapped_column(Integer, ForeignKey("educacao.usuario.id", ondelete="CASCADE"), nullable=False)
    lista_itens: Mapped[List[Dict[str, Any]]] = mapped_column(JSONB, nullable=False)
    quantidade_meninas: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    quantidade_meninos: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    id_user_apoiador: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("educacao.usuario.id", ondelete="SET NULL"), nullable=True)
    status: Mapped[SolicitacaoStatus] = mapped_column(
        SQLEnum(
            SolicitacaoStatus,
            values_callable=lambda enum: [e.value for e in enum]
        ),
        nullable=False,
        default=SolicitacaoStatus.CRIADO
    )
    dt_criada: Mapped[datetime] = mapped_column(DateTime,default=datetime.now, nullable=False)
    dt_finalizada: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)