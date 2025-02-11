from pydantic import BaseModel

class BebidaCreate(BaseModel):
    nombre: str
    descripcion: str
    estatus: bool
    cantidad_stock: float
  
class Bebida(BaseModel):
    id: int
    nombre: str
    descripcion: str
    estatus: bool
    cantidad_stock: float
    class Config:
        from_attributes = True