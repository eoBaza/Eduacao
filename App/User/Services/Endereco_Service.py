import brazilcep

#Arquivos
from App.User.Models.Endereco import Endereco
from App.User.Models.Regiao import Regiao
from Database.Database import SessionLocal
from fastapi import HTTPException
from sqlalchemy.orm import Session

def get_endereco_by_cep(cep: str) -> dict:
    endereco = brazilcep.get_address_from_cep(cep)
    #print(endereco)
    return endereco

def create_endereco(cep: str, numero: str, complemento:str, db: Session ) -> Endereco:
    address  = get_endereco_by_cep(cep)
    uf_cep = address["uf"]
    regiao = db.query(Regiao).filter(Regiao.uf == uf_cep).first()
    if not regiao:
        raise HTTPException(status_code=440, detail=f"Região para a UF '{uf_cep}' não cadastrada.")

    new_address = Endereco(
        endereco=address["street"],
        complemento=complemento or address["complement"],
        cep=address["cep"],
        numero=numero,
        id_regiao=regiao.id
    )
    db.add(new_address)
    db.commit()
    db.refresh(new_address)

    return new_address
