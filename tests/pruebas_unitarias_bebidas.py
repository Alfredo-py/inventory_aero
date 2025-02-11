from fastapi.testclient import TestClient
from unittest.mock import MagicMock
from fastapi import HTTPException
from src.main import app
from src.repositories.bebidas_repository import BebidaRepository

client = TestClient(app)

# Mock del repositorio
mock_repo = MagicMock(BebidaRepository)
app.dependency_overrides[BebidaRepository] = lambda: mock_repo

def test_crear_bebida():
    mock_repo.crear_bebida.return_value = {"message": "Bebida creado"}
    response = client.post("/api/v1/bebidas/", json={
        "nombre": "Manzana",
        "descripcion": "Fruta roja",
        "estatus": True,
        "cantidad_stock": 10
    })
    assert response.status_code == 200
    assert response.json() == {"detail": "Bebida creada"}

def test_crear_bebida_repetido():
    def mock_crear_bebida(*args, **kwargs):
        raise HTTPException(status_code=409, detail="La bebida ya existe")
    
    mock_repo.crear_bebida.side_effect = mock_crear_bebida
    response = client.post("/api/v1/bebidas/", json={
        "nombre": "Manzana",
        "descripcion": "Fruta roja",
        "estatus": True,
        "cantidad_stock": 10
    })
    assert response.status_code == 409
    assert response.json()["detail"] == "La bebida ya existe"

# Nuevas pruebas agregadas

def test_crear_bebida_nombre_vacio():
    response = client.post("/api/v1/bebidas/", json={
        "nombre": "",  # Nombre vacío
        "descripcion": "Fruta roja",
        "estatus": True,
        "cantidad_stock": 10
    })
    assert response.status_code == 422  # Error de validación
    assert "detail" in response.json()

def test_crear_bebida_stock_negativo():
    response = client.post("/api/v1/bebidas/", json={
        "nombre": "Pera",
        "descripcion": "Fruta roja",
        "estatus": True,
        "cantidad_stock": -5  # Stock negativo
    })
    assert response.status_code == 422  # Error de validación
    assert "detail" in response.json()

def test_crear_bebida_sin_descripcion():
    response = client.post("/api/v1/bebidas/", json={
        "nombre": "Manzana",
        "estatus": True,
        "cantidad_stock": 10  # Falta la descripción
    })
    assert response.status_code == 422  # Error de validación
    assert "detail" in response.json()

def test_obtener_bebida():
    mock_repo.obtener_bebida.return_value = {
        "id": 1,
        "nombre": "Manzana",
        "descripcion": "Fruta roja",
        "estatus": True,
        "cantidad_stock": 10
    }
    response = client.get("/api/v1/bebidas/1")
    assert response.status_code == 200
    assert response.json()["nombre"] == "Manzana"

def test_obtener_bebida_no_encontrado():
    mock_repo.obtener_bebida.return_value = None
    response = client.get("/api/v1/bebidas/99")
    assert response.status_code == 404
    assert response.json()["detail"] == "Bebida no encontrado"



