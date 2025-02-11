# src/test_db.py
from src.utils.database import Base, engine

# Crear las tablas en la base de datos
Base.metadata.create_all(bind=engine)