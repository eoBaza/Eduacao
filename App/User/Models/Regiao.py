from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from Database.Database import Base


class Regiao(Base):
    __tablename__ = "regiao"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    estado: Mapped[str] = mapped_column(String(255), nullable=False)
    uf: Mapped[str] = mapped_column(String(4), nullable=True)
    
    