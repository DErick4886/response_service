from fastapi import FastAPI
from routes import preguntas
from database import Base, engine
from fastapi.middleware.cors import CORSMiddleware
from routes import responder


# Crear las tablas en la base de datos (si no existen)
Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Incluir el router de preguntas
app.include_router(preguntas.router)
app.include_router(responder.router)
