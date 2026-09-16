from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from typing import List

#Arquivos 
from Database.Database import get_db
from Solicitacao.Schemas.Solicitacao import *
from Solicitacao.Models.Solicitacao import Solicitacao
from User.Models.Usuario import Usuario

router  = APIRouter()

@router.get("/solicitacao", response_model=List[SolicitacaoReponse])
def get_all_solicitacoes(db: Session = Depends(get_db)):
    all_solicitacoes = db.query(Solicitacao).all()
    
    if not all_solicitacoes:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Nao existe solicitacoes"
        )

    return all_solicitacoes

@router.post("/solicitacao/create/", response_model=SolicitacaoReponse)
def create_solicitacao(dados: SolicitacaoCreate,db: Session = Depends(get_db)):
    user_db = db.query(Usuario).filter(Usuario.id == dados.id_user_requerente).first()
    if not user_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario nao encontrado"
        )
    try:    
        new_solicitacao = Solicitacao(
            id_user_requerente = user_db.id,
            lista_itens = dados.lista_itens,
            quantidade_meninas = dados.quantidade_meninas,
            quantidade_meninos = dados.quantidade_meninos
        )    
        db.add(new_solicitacao)
        db.commit()
        db.refresh(new_solicitacao)

        return new_solicitacao
        
    except HTTPException:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Erro ao criar solicitação")
