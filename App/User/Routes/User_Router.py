from Database.Database import get_db
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException,status
from pydantic import EmailStr

#Arquivos
from User.Schemas.Usuario import *
from User.Models.Usuario import Usuario
from User.Services.User_Service import hash_password, verifica_password
from User.Services.Endereco_Service import create_endereco
from User.Services.UserSessao_Service import create_session_user

router = APIRouter()

@router.post("/user/signup/", response_model=UsuarioResponse)
def create_user(nome:str, gmail: EmailStr, tipo_usuario: str, cnpj_cpf: str, senha:str ,cep: str, numero: str, complemento:str | None = None, db: Session = Depends(get_db)):
    senha_cript = hash_password(senha)

    novo_endereco = create_endereco(cep, numero, complemento, db=db)

    usuario = Usuario(
        nome=nome, 
        gmail=gmail,
        tipo_usuario=tipo_usuario,
        cnpj_cpf=cnpj_cpf,
        senha_hash=senha_cript,
        id_endereco=novo_endereco.id
    )
    db.add(usuario)
    db.commit()
    db.refresh(usuario)
    return usuario

@router.post("/login/", response_model=LoginResponse)
def login(gmail: str, senha: str, db: Session = Depends(get_db)):
    try:
        user_email = db.query(Usuario).filter(Usuario.gmail == gmail).first()
        if not user_email:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail=f"E-mail '{gmail}' não encontrado."
            )
        user_senha = user_email.senha_hash
        senha_cript = verifica_password(senha, user_senha)
        if senha_cript:
            token_sessao = create_session_user(user_email.id, db=db)
            return {"message":"Login Sucesso",
                    "Session_Code":f"{token_sessao.sessao_code}"}
        return {"Message": "Senha incorreta, favor informar novamente."}
    except HTTPException:
        return {HTTPException}