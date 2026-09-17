from Database.Database import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String

class Vw_usuario_Info(Base):
    __tablename__ = "vw_usuario_info"
    __table_args__ = {"schema": "educacao"}

    id_usuario: Mapped[int] = mapped_column(Integer, primary_key = True)
    nome: Mapped[str] = mapped_column(String(255), nullable= False)
    gmail: Mapped[str] = mapped_column(String(255), nullable= True)
    tipo_usuario: Mapped[str] = mapped_column(String(1), nullable= False)
    cnpj_cpf: Mapped[str] = mapped_column(String(20), nullable=True)
    cep: Mapped[str] = mapped_column(String(9), nullable=False)
    endereco: Mapped[str] = mapped_column(String(255), nullable=False)
    numero: Mapped[str] = mapped_column(String(20), nullable=False)
    complemento: Mapped[str] = mapped_column(String(255), nullable=False)

