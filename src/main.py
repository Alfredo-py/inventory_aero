from fastapi import FastAPI
from src.api.v1.alimentos import router as alimentos_router
from src.api.v1.bebidas import router as bebidas_router

from src.utils.database import create_tables  

app = FastAPI()

app.include_router(alimentos_router, prefix="/api/v1")
app.include_router(bebidas_router, prefix="/api/v1")

@app.get("/")
def read_root():
    return {"message": "Bienvenido al sistema de inventario"}