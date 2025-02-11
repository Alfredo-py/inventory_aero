from pydantic import BaseModel

class AlimentoCreate(BaseModel):
    nombre: str
    descripcion: str
    estatus: bool
    cantidad_stock: float

class Alimento(BaseModel):
    id: int
    nombre: str
    descripcion: str
    estatus: bool
    cantidad_stock: float

    class Config:
        from_attributes = True