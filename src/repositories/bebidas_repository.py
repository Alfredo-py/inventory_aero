from src.utils.database import get_connection
from fastapi import HTTPException

class BebidaRepository:
    def crear_bebida(self, nombre: str, descripcion: str, estatus: bool, cantidad_stock: float):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM bebidas WHERE nombre = ?",(nombre,))
        bebida = cursor.fetchone()
        if bebida:
            raise HTTPException(status_code=409, detail="La bebida ya existe")
        else:
            if not nombre:
                raise HTTPException(status_code=422, detail="campo vacio")
            if cantidad_stock < 0:
                raise HTTPException(status_code=422, detail="ingresaste stock negativo")
            cursor.execute(
                "INSERT INTO bebidas (nombre, descripcion, estatus, cantidad_stock) VALUES (?, ?, ?, ?)",
                (nombre, descripcion, estatus, cantidad_stock)
            )
            conn.commit()
        cursor.close()
        conn.close()
        raise HTTPException(status_code=200, detail="Bebida creada")
    def obtener_bebida(self, id: int):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM bebidas WHERE id = ?", (id,))
        bebida = cursor.fetchone()
        cursor.close()
        conn.close()

        if bebida:
            id, nombre, descripcion, estatus, cantidad_stock = bebida
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
            
    
    def actualizar_bebida(self, id: int, nombre: str = None, descripcion: str = None, estatus: bool = None, cantidad_stock: float = None):
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
            query = f"UPDATE bebidas SET {', '.join(updates)} WHERE id = ?"
            cursor.execute(query, params)

            # Confirmar la transacción
            conn.commit()
            raise HTTPException(status_code=200, detail="Elmento actualizado correctamente")
        except Exception as e:
            #print(f"Error al actualizar el alimento: {e}")
            raise HTTPException(status_code=400, detail="Error al actualizar la bebida")
        finally:
            # Cerrar el cursor y la conexión
            cursor.close()
            conn.close()

    def del_bebida(self,nombre: str):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT id FROM bebidas WHERE nombre = ?", (nombre,))
        bebida = cursor.fetchone()

        if bebida:
            cursor.execute("DELETE FROM bebidas WHERE nombre = ?", (nombre,))
            conn.commit()
            raise HTTPException(status_code=200, detail="Elmento borrado correctamente")
            
        else:
            cursor.close()
            conn.close()
            raise HTTPException(status_code=404, detail="El elemento no existe en la base de datos")

        