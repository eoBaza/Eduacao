from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from Database.Database import Base

class Usuario(Base):
    __tablename__ = "usuario"
    __table_args__ = {"schema": "educacao"}

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nome: Mapped[str] = mapped_column(String(255), nullable=False)
    gmail: Mapped[str | None] = mapped_column(String(255), nullable=True, unique=True)
    id_tipo_usuario: Mapped[int] = mapped_column(Integer, ForeignKey("educacao.tipo_usuario.id"), nullable=False)
    cnpj_cpf: Mapped[str] = mapped_column(String(20), nullable=False)
    senha_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    id_endereco: Mapped[int | None] = mapped_column(Integer, ForeignKey("educacao.endereco.id"), nullable=True)