from Database.Database import get_db
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException,status
from pydantic import EmailStr

#Arquivos
from User.Schemas.Usuario import *
from User.Models.Usuario import Usuario
from User.Services.User_Service import hash_password, verifica_password, reset_password
from User.Services.Endereco_Service import create_endereco
from User.Services.UserSessao_Service import create_session_user

router = APIRouter()

@router.post("/user/signup/", response_model=UsuarioResponse)
def create_user(dados: UsuarioCreate,cep: str, numero: str, complemento:str | None = None, db: Session = Depends(get_db)):
    senha_cript = hash_password(dados.senha)

    novo_endereco = create_endereco(cep, numero, complemento, db=db)

    usuario = Usuario(
        nome=dados.nome, 
        gmail=dados.gmail,
        tipo_usuario=dados.tipo_usuario,
        cnpj_cpf=dados.cnpj_cpf,
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

@router.post("/user/reset-password/", response_model=ResetSenhaResponse)
def reset_senha(dados: ResetSenha, db: Session = Depends(get_db)):

    usuario_db = db.query(Usuario).filter(Usuario.gmail == dados.gmail).first()

    if not usuario_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"E-mail '{dados.gmail}' não encontrado."
        )

    if not reset_password(dados.senha, dados.confirma_senha):
        raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="As senhas não coincidem."
    )
        
    usuario_db.senha_hash = hash_password(dados.senha)
    db.commit()
    return {"message": "Senha alterada com sucesso."}
      
    

