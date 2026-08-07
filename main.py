# pip installa FastAPI uvicorn
from fastapi import FastAPI

# Validación de datos con pydantic
from pydantic import BaseModel

# Importar para usar CORS
from fastapi.middleware.cors import CORSMiddleware

# WebSocket
from fastapi import WebSocket

#
from src.routes.auth_routes import app as auth_routes

class Item(BaseModel):
    name:str
    edad:int

app = FastAPI()

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_routes, prefix="/auth", tags=["auth"])

# Middleware
@app.middleware("http")
async def add_custom_header(request, call_next):
    response = await call_next(request)
    response.headers['X-Custom-Header'] = 'CustomValue'
    return response

# Un funciono que se ejecuta una vez se arranque la aplicación
@app.on_event("startup")
async def startup_event():
    # Para levantar un servicio o una base de datos
    print("Aplicación arrancando/ Levantando proyecto ...")

# Cerrar
@app.on_event("shutdown")
async def shutdown_event():
    print("Aplicación cerrada")

@app.get('/')
async def read_root():
    return {"message": "Hello, World!"}
# uvicorn main:app -- reload
# reload nos ayuda a que nuestro servidor se refresque cada vez que actualicemos codigo sin tener que detener el proyecto y volver a correr
# Te permite crear el swagger http://127.0.0.1:8000/docs
# http://127.0.0.1:8000/docs#/

@app.post('/items')
async def create_item(item: Item):
    return {'item': item, 'name': item.name, 'edad': item.edad}

connected_clients = []
@app.websocket("/ws/data")
async def websocket_data(websocket: WebSocket):
    await websocket.accept() # Cuando el frontend nos solicita una conexion se la aceptamos
    # La añadimos a la lista de los clientes que estan conectados
    connected_clients.append(websocket)
    try:
        while True:
            await websocket.receive_text()
    except:
        connected_clients.remove(websocket)