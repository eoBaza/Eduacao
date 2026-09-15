from pydantic import BaseModel

# Retorno para API GET para mostrar os itens
class ItensResponse(BaseModel):
    id: int
    nome_item: str
    imagem_item: str | None = None

    class Config:
        from_attributes: True