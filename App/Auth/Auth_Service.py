from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

# Arquivos
from Database.Database import get_db
from User.Models.Usuario_Sessao import Usuario_Sessao

security = HTTPBearer()

def get_usuario_logado(credentials: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_db)):
    token = credentials.credentials
    sessao = db.query(Usuario_Sessao).filter(Usuario_Sessao.sessao_code == token, Usuario_Sessao.ativo == True).first()

    if not sessao:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token Invalido ou sessao inativa."
        )

    return sessao