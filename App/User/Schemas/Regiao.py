from pydantic import BaseModel

class RegiaoResponse(BaseModel):
    id: int
    estado: str
    uf: str