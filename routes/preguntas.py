from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from models.pregunta import Pregunta
from schemas.pregunta import RespuestasUsuario
from models.control import Control
from database import get_db

router = APIRouter()

# Obtener las preguntas del cuento (GET)
@router.get("/v1/cuento/pregunta/{id_cuento}", response_model=dict)
def obtener_preguntas(id_cuento: int, db: Session = Depends(get_db)):
    """
    Obtiene las preguntas asociadas a un cuento determinado.
    """
    preguntas = db.query(Pregunta).filter(Pregunta.id_cuento == id_cuento).all()

    if not preguntas:
        raise HTTPException(status_code=404, detail="No se encontraron preguntas para este cuento")

    preguntas_data = [
        {"id_pregunta": pregunta.id_pregunta, "contenido": pregunta.contenido, "resp_correcta": pregunta.resp_correcta}
        for pregunta in preguntas
    ]

    return {
        "message": "Preguntas obtenidas exitosamente",
        "status": 200,
        "data": preguntas_data
    }
