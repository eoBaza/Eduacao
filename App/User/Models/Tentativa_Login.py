from Database.Database import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String, DateTime

class TentativaLogin(Base):
    __tablename__ = "tentativa_login"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    id_user: Mapped[int] = mapped_column(Integer, nullable=False)
    status: Mapped[str] = mapped_column(String(255), nullable=False)
    ip_address: Mapped[str] = mapped_column(String(255), nullable=True)
    navegador_agent: Mapped[str] = mapped_column(String(255), nullable=True)
    dt_criada: Mapped[DateTime] = mapped_column(DateTime, nullable=False)