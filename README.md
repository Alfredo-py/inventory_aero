# FastAPI Inventario - Instalación y Uso

## Requisitos
- Python 3.12
- Java 17
- Docker (Opcional, para contenedores)

## 🚀 Instalación Manual
1. Crea un entorno virtual e instala dependencias:
   ```sh
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```
2. Ejecuta la aplicación:
   ```sh
   uvicorn src.main:app --host 0.0.0.0 --port 8000
   ```
3. Accede a la API en el navegador:
   - Documentación: [http://localhost:8000/docs](http://localhost:8000/docs)

## 🐳 Instalación con Docker
1. Construye la imagen:
   ```sh
   docker build -t fastapi-h2-app .
   ```
2. Ejecuta el contenedor:
   ```sh
   docker run -p 8000:8000 fastapi-h2-app
   ```
3. Accede a la API en el navegador:
   - [http://localhost:8000/docs](http://localhost:8000/docs)

¡Listo! La API está en funcionamiento, recuerda ver la documentacion en http://127.0.0.1:8000/docs.


