from src.utils.database import get_connection
from fastapi import HTTPException

class AlimentoRepository:
    def crear_alimento(self, nombre: str, descripcion: str, estatus: bool, cantidad_stock: float):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM alimentos WHERE nombre = ?",(nombre,))
        alimento = cursor.fetchone()
        if alimento:
            raise HTTPException(status_code=409, detail="El alimento ya existe")
            #return {"message": "El alimento ya existe"}
        else:
            if not nombre:
                raise HTTPException(status_code=422, detail="campo vacio")
            if cantidad_stock < 0:
                raise HTTPException(status_code=422, detail="ingresaste stock negativo")
            cursor.execute(
                "INSERT INTO alimentos (nombre, descripcion, estatus, cantidad_stock) VALUES (?, ?, ?, ?)",
                (nombre, descripcion, estatus, cantidad_stock)
            )    
            conn.commit()
        cursor.close()
        conn.close()
        raise HTTPException(status_code=200, detail="Alimento creado")
    def obtener_alimento(self, id: int):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM alimentos WHERE id = ?", (id,))
        alimento = cursor.fetchone()

        cursor.close()
        conn.close()

        if alimento:
            id, nombre, descripcion, estatus, cantidad_stock = alimento
            nombre = str(nombre) if nombre else ""
            descripcion = str(descripcion) if descripcion else ""

            return {
                "id": id,
                "nombre": nombre,
                "descripcion": descripcion,
                "estatus": bool(estatus),
                "cantidad_stock": float(cantidad_stock)
            }
        else:
            return None
            
    
    def actualizar_alimento(self, id: int, nombre: str = None, descripcion: str = None, estatus: bool = None, cantidad_stock: float = None):
        conn = get_connection()
        cursor = conn.cursor()

        try:
            updates = []
            params = []

            if nombre is not None:
                updates.append("nombre = ?")
                params.append(nombre)
            if descripcion is not None:
                updates.append("descripcion = ?")
                params.append(descripcion)
            if estatus is not None:
                updates.append("estatus = ?")
                params.append(estatus)
            if cantidad_stock is not None:
                updates.append("cantidad_stock = ?")
                params.append(cantidad_stock)

            # Si no hay campos para actualizar, salir
            if not updates:
                print("No se proporcionaron campos para actualizar.")
                return

            # Agregar el ID al final de los parámetros
            params.append(id)

            # Construir la consulta SQL final
            query = f"UPDATE alimentos SET {', '.join(updates)} WHERE id = ?"
            cursor.execute(query, params)

            # Confirmar la transacción
            conn.commit()
            #print(f"Alimento con ID {id} actualizado correctamente.")
            raise HTTPException(status_code=200, detail="Elmento actualizado correctamente")
        except Exception as e:
            #print(f"Error al actualizar el alimento: {e}")
            raise HTTPException(status_code=400, detail="Error al actualizar el alimento")
        finally:
            # Cerrar el cursor y la conexión
            cursor.close()
            conn.close()

    def del_alimento(self,nombre: str):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT id FROM alimentos WHERE nombre = ?", (nombre,))
        alimento = cursor.fetchone()

        if alimento:
            cursor.execute("DELETE FROM alimentos WHERE nombre = ?", (nombre,))
            conn.commit()
            raise HTTPException(status_code=200, detail="Elmento borrado correctamente")
            
        else:
            cursor.close()
            conn.close()
            raise HTTPException(status_code=404, detail="El elemento no existe en la base de datos")
            #print(f"El alimento '{nombre}' no existe en la base de datos.")

        