from sqlalchemy import Integer, String,ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from Database.Database import Base

class Endereco(Base):
    __tablename__ = "endereco"
    __table_args__ = {"schema": "educacao"}

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    endereco: Mapped[str] = mapped_column(String(255), nullable=False)
    complemento: Mapped[str] = mapped_column(String(255), nullable=True)
    cep: Mapped[str] = mapped_column(String(9), nullable=False)
    numero: Mapped[str] = mapped_column(String(20), nullable=False)
    id_regiao: Mapped[int] = mapped_column(Integer, ForeignKey("educacao.regiao.id"),nullable=False)





