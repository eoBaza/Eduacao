from Database.Database import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String, Boolean, DateTime
from datetime import datetime


class Usuario_Sessao(Base):
    __tablename__ = "usuario_sessao"

    id: Mapped[int] =mapped_column(Integer, primary_key=True, autoincrement=True)
    id_usuario: Mapped[int] = mapped_column(Integer, nullable=False)
    ativo: Mapped[bool] = mapped_column(Boolean, nullable=False)
    dt_expirado: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    sessao_code: Mapped[str] = mapped_column(String(50),unique=True, nullable=False)
    dt_criada: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    