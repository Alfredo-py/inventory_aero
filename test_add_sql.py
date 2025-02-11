# src/test_insert.py
from src.utils.database import get_connection

# Obtener una conexión
conn = get_connection()
cursor = conn.cursor()

# Insertar un alimento
cursor.execute(
    "INSERT INTO alimentos (nombre, descripcion, estatus, cantidad_stock) VALUES (?, ?, ?, ?)",
    ("Manzana", "Fruta roja", True, 100.0)
)

# Confirmar la transacción
conn.commit()

# Consultar los alimentos
cursor.execute("SELECT * FROM alimentos")
alimentos = cursor.fetchall()
print("Alimentos en la base de datos:", alimentos)

# Cerrar la conexión
cursor.close()
conn.close()