from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column
from Database.Database import Base

class Itens(Base):
    __tablename__ = "itens"
    __table_args__ = {"schema": "educacao"}

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nome_item: Mapped[str] = mapped_column(String(100), nullable=True)
    imagem_item: Mapped[str] = mapped_column(String(255), nullable=False)