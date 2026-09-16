from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

#Arquivos
from Itens.Models.Itens import Itens
from Itens.Schemas.Itens import ItensResponse
from Database.Database import get_db as db


router = APIRouter()


@router.get("/list_itens", response_model=List[ItensResponse])
def list_itens(db:Session = Depends(db)):
    itens = db.query(Itens).all()
    if not itens:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail="Nao foi encontrado itens."
        )
    return itens