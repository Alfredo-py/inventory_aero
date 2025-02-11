import jaydebeapi
import jpype
import os

# Configuración de la conexión a H2
H2_DRIVER = "org.h2.Driver"
H2_URL = "jdbc:h2:file:./inventario"  
H2_USER = "sa"  
H2_PASSWORD = ""  
H2_JAR_PATH = "src/drivers/h2-2.3.232.jar" 


# Verificar que el archivo JAR exista
if not os.path.exists(H2_JAR_PATH):
    raise FileNotFoundError(f"No se encontró el archivo JAR en la ruta: {H2_JAR_PATH}")

# Iniciar la JVM
if not jpype.isJVMStarted():
    jpype.startJVM(classpath=[H2_JAR_PATH])

# Función para obtener una conexión a la base de datos
def get_connection():
    conn = jaydebeapi.connect(
        H2_DRIVER,
        H2_URL,
        [H2_USER, H2_PASSWORD],
        H2_JAR_PATH,
    )
    return conn

# Función para crear las tablas
def create_tables():
    conn = get_connection()
    cursor = conn.cursor()

    # Crear la tabla 'alimentos'
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS alimentos (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nombre VARCHAR(255) NOT NULL,
            descripcion VARCHAR(255),
            estatus BOOLEAN DEFAULT TRUE,
            cantidad_stock FLOAT DEFAULT 0.0
        )
    """)

    # Crear la tabla 'bebidas'
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS bebidas (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nombre VARCHAR(255) NOT NULL,
            descripcion VARCHAR(255),
            estatus BOOLEAN DEFAULT TRUE,
            cantidad_stock FLOAT DEFAULT 0.0 
        )
    """)

    # Crear la tabla 'movimientos'
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS movimientos (
            id INT AUTO_INCREMENT PRIMARY KEY,
            alimento_id INT,
            bebida_id INT,
            cantidad FLOAT,
            tipo VARCHAR(50),
            fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (alimento_id) REFERENCES alimentos(id),
            FOREIGN KEY (bebida_id) REFERENCES bebidas(id)

        )
    """)

    conn.commit()
    cursor.close()
    conn.close()

# Crear las tablas al importar este módulo
create_tables()