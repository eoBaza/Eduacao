from Database.Database import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String, Boolean, DateTime
from datetime import datetime

class VeiculoMotorista(Base):
    __tablename__ = "veiculo_motorista"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    id_usuario: Mapped[int] = mapped_column(Integer, nullable=False)
    placa: Mapped[str] = mapped_column(String(10), nullable=False)