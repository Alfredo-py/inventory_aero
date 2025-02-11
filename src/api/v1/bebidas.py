from fastapi import APIRouter, Depends, HTTPException
from src.repositories.bebidas_repository import BebidaRepository

from src.schemas.bebidas import BebidaCreate

router = APIRouter()
    
@router.post("/bebidas/")
def crear_bebida(bebida: BebidaCreate):
    repository = BebidaRepository()
    return repository.crear_bebida(
        nombre=bebida.nombre,
        descripcion=bebida.descripcion,
        estatus=bebida.estatus,
        cantidad_stock=bebida.cantidad_stock
    )

@router.get("/bebidas/{id}")
def obtener_bebida(id: int):
    repository = BebidaRepository()
    bebida = repository.obtener_bebida(id)
    if bebida:
        return bebida
    raise HTTPException(status_code=404, detail="Bebida no encontrado")

@router.put("/actualizar_bebidas/")
def actualizar_bebida(id: int, nombre: str = None, descripcion: str = None, estatus: bool = None, cantidad_stock: float = None):
    repository = BebidaRepository()
    bebida = repository.actualizar_bebida(id,nombre,descripcion,estatus,cantidad_stock)
    if bebida:
        return bebida


@router.delete("/del_bebidas/{nombre}")
def del_bebida(nombre: str):
    repository = BebidaRepository()
    bebida = repository.del_bebida(nombre)
    if bebida:
        return bebida
    

