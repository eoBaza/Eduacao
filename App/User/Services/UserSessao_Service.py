import secrets, os
from dotenv import load_dotenv
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from fastapi import Depends

# Arquivos 
from User.Models.Usuario_Sessao import Usuario_Sessao
from User.Models.Usuario import Usuario
from Database.Database import get_db 


load_dotenv()
nbytes = int(os.getenv("nbytes"))
time_expira = int(os.getenv("expira_time"))

def gerar_session_code(nbytes: int = nbytes) -> str:
    return secrets.token_hex(nbytes)


def create_session_user(user_id: int, db: Session = Depends(get_db)):
    dt_now= datetime.now()
    dt_exp = dt_now + timedelta(days=time_expira)
    code_sessao = gerar_session_code()

    usuario = db.query(Usuario).filter(Usuario.id == user_id).first()
    if not usuario:
        raise ValueError("Usuario nao encontrado para criar sessao")
    usuario_sessao = Usuario_Sessao(
        id_usuario=user_id,
        ativo=True,
        dt_expira=dt_exp,
        sessao_code=code_sessao,
        dt_criada=dt_now
    )
    db.add(usuario_sessao)
    db.commit()
    db.refresh(usuario_sessao)
    
    return usuario_sessao