from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from typing import List

#Arquivos 
from Database.Database import get_db
from Solicitacao.Schemas.Solicitacao import *
from Solicitacao.Models.Solicitacao import Solicitacao
from Solicitacao.Models.Vw_SolicitacaoPendente import Vw_SolicitacaoPendente
from User.Models.Usuario import Usuario
from User.Models.Usuario_Sessao import Usuario_Sessao
from Auth.Auth_Service import get_usuario_logado

router  = APIRouter()

@router.get("/solicitacao/", response_model=List[SolicitacaoReponse])
def get_all_solicitacoes(db: Session = Depends(get_db)):
    all_solicitacoes = db.query(Solicitacao).all()
    
    if not all_solicitacoes:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Nao existe solicitacoes"
        )

    return all_solicitacoes

@router.post("/solicitacao/create/", response_model=SolicitacaoReponse)
def create_solicitacao(dados: SolicitacaoCreate,session: Usuario_Sessao = Depends(get_usuario_logado),db: Session = Depends(get_db)):
    user_db = db.query(Usuario).filter(Usuario.id == session.id_usuario).first()
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

@router.get("/solicitacao/minha-solicitacao/", response_model=List[SolicitacaoReponse])
def get_my_solicitacao(session: Usuario_Sessao = Depends(get_usuario_logado), db: Session = Depends(get_db)):
    get_my_solicitacao = (db.query(Solicitacao).filter(Solicitacao.id_user_requerente == session.id_usuario).all())

    return get_my_solicitacao

@router.get("/solicitacao/pendente/", response_model=list[Vw_SolicitacaoPendenteResponse])
def get_solicitacoes_pendent(session: Usuario_Sessao = Depends(get_usuario_logado),db: Session = Depends(get_db)):
    user_name = db.query(Usuario).filter(Usuario.id == session.id).first()
    solicitacao = (db.query(Vw_SolicitacaoPendente).filter(Vw_SolicitacaoPendente.usuario_requerente == user_name.nome).all())

    return solicitacao

@router.get("/solicitacao/{solicitacao_id}/",response_model=SolicitacaoReponse)
def get_solicitacao(solicitacao_id: int,db: Session = Depends(get_db)):
    solicitacao = (
        db.query(Solicitacao)
        .filter(Solicitacao.id == solicitacao_id)
        .first()
    )

    if not solicitacao:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Solicitação não encontrada."
        )

    return solicitacao



