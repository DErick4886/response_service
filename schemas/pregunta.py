from pydantic import BaseModel
from typing import List
from typing import Dict

class PreguntaBase(BaseModel):
    id_pregunta: int
    id_cuento: int
    contenido: str
    resp_correcta: bool  # Cambiado a booleano

class RespuestaPreguntas(BaseModel):
    message: str
    status: int
    data: List[PreguntaBase]

class RespuestasUsuario(BaseModel):
    respuestas: str#Dict[str, bool]  # Mapea el id_pregunta a la respuesta (True/False)