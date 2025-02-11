from fastapi import APIRouter, Depends, HTTPException
from src.repositories.alimento_repository import AlimentoRepository

from src.schemas.alimento import AlimentoCreate

router = APIRouter()

@router.post("/alimentos/")
def crear_alimento(alimento: AlimentoCreate):
    repository = AlimentoRepository()
    return repository.crear_alimento(
        nombre=alimento.nombre,
        descripcion=alimento.descripcion,
        estatus=alimento.estatus,
        cantidad_stock=alimento.cantidad_stock
    )
    

@router.get("/alimentos/{id}")
def obtener_alimento(id: int):
    repository = AlimentoRepository()
    alimento = repository.obtener_alimento(id)
    if alimento:
        return alimento
    raise HTTPException(status_code=404, detail="Alimento no encontrado")

@router.put("/actualizar_alimentos/")
def actualizar_alimento(id: int, nombre: str = None, descripcion: str = None, estatus: bool = None, cantidad_stock: float = None):
    repository = AlimentoRepository()
    alimento = repository.actualizar_alimento(id,nombre,descripcion,estatus,cantidad_stock)
    if alimento:
        return alimento


@router.delete("/del_alimentos/{nombre}")
def del_alimento(nombre: str):
    repository = AlimentoRepository()
    alimento = repository.del_alimento(nombre)
    if alimento:
        return alimento
  