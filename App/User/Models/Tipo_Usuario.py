from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from Database.Database import Base


class TipoUsuario(Base):
    __tablename__ = "tipo_usuario"
    __table_args__ = {"schema": "educacao"}

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    nome: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    descricao: Mapped[str] = mapped_column(
        String(250),
        nullable=False
    )