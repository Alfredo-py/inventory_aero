from fastapi.testclient import TestClient
from unittest.mock import MagicMock
from fastapi import HTTPException
from src.main import app
from src.repositories.alimento_repository import AlimentoRepository

client = TestClient(app)

# Mock del repositorio
mock_repo = MagicMock(AlimentoRepository)
app.dependency_overrides[AlimentoRepository] = lambda: mock_repo

def test_crear_alimento():
    mock_repo.crear_alimento.return_value = {"message": "Alimento creado"}
    response = client.post("/api/v1/alimentos/", json={
        "nombre": "Manzana",
        "descripcion": "Fruta roja",
        "estatus": True,
        "cantidad_stock": 10
    })
    assert response.status_code == 200
    assert response.json() == {"detail": "Alimento creado"}

def test_crear_alimento_repetido():
    def mock_crear_alimento(*args, **kwargs):
        raise HTTPException(status_code=409, detail="El alimento ya existe")
    
    mock_repo.crear_alimento.side_effect = mock_crear_alimento
    response = client.post("/api/v1/alimentos/", json={
        "nombre": "Manzana",
        "descripcion": "Fruta roja",
        "estatus": True,
        "cantidad_stock": 10
    })
    assert response.status_code == 409
    assert response.json()["detail"] == "El alimento ya existe"

# Nuevas pruebas agregadas

def test_crear_alimento_nombre_vacio():
    response = client.post("/api/v1/alimentos/", json={
        "nombre": "",  # Nombre vacío
        "descripcion": "Fruta roja",
        "estatus": True,
        "cantidad_stock": 10
    })
    assert response.status_code == 422  # Error de validación
    assert "detail" in response.json()

def test_crear_alimento_stock_negativo():
    response = client.post("/api/v1/alimentos/", json={
        "nombre": "Pera",
        "descripcion": "Fruta roja",
        "estatus": True,
        "cantidad_stock": -5  # Stock negativo
    })
    assert response.status_code == 422  # Error de validación
    assert "detail" in response.json()

def test_crear_alimento_sin_descripcion():
    response = client.post("/api/v1/alimentos/", json={
        "nombre": "Manzana",
        "estatus": True,
        "cantidad_stock": 10  # Falta la descripción
    })
    assert response.status_code == 422  # Error de validación
    assert "detail" in response.json()

def test_obtener_alimento():
    mock_repo.obtener_alimento.return_value = {
        "id": 1,
        "nombre": "Manzana",
        "descripcion": "Fruta roja",
        "estatus": True,
        "cantidad_stock": 10
    }
    response = client.get("/api/v1/alimentos/1")
    assert response.status_code == 200
    assert response.json()["nombre"] == "Manzana"

def test_obtener_alimento_no_encontrado():
    mock_repo.obtener_alimento.return_value = None
    response = client.get("/api/v1/alimentos/99")
    assert response.status_code == 404
    assert response.json()["detail"] == "Alimento no encontrado"



