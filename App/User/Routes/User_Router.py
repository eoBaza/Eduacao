from Database.Database import get_db
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends
from pydantic import EmailStr

#Arquivos
from User.Schemas.Usuario import UsuarioResponse
from User.Models.Usuario import Usuario
from User.Services.User_Service import hash_password

router = APIRouter()

@router.post("/user/signup/", response_model=UsuarioResponse)
def create_user(nome:str, gmail: EmailStr, tipo_usuario: str, cnpj_cpf: str, senha:str ,db: Session = Depends(get_db)):
    senha_cript = hash_password(senha)

    usuario = Usuario(
        nome=nome, 
        gmail=gmail,
        tipo_usuario=tipo_usuario,
        cnpj_cpf=cnpj_cpf,
        senha_hash=senha_cript
    )
    db.add(usuario)
    db.commit()
    db.refresh(usuario)
    return usuario