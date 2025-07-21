from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from models.pregunta import Pregunta
from schemas.pregunta import RespuestasUsuario
from models.control import Control
from database import get_db

router = APIRouter()

# Enviar las respuestas del usuario (POST)

@router.post("/v1/cuento/resultado/{id_cuento}/{id_usuario}", response_model=dict)
def enviar_respuestas(id_cuento: int, id_usuario: int, respuestas_usuario: RespuestasUsuario, db: Session = Depends(get_db)):
    """
    Recibe las respuestas del usuario como string "SI,NO,SI,NO,SI", las compara con las respuestas correctas,
    y guarda el número de respuestas correctas en el campo 'estrella' de la tabla 'control' en la base de datos.
    """
    preguntas = db.query(Pregunta).filter(Pregunta.id_cuento == id_cuento).order_by(Pregunta.id_pregunta).all()
    
    print(f"Preguntas encontradas: {len(preguntas)} para el cuento con id {id_cuento}")

    if not preguntas:
        raise HTTPException(status_code=404, detail="No se encontraron preguntas para este cuento")

    # Procesar las respuestas del usuario desde el string
    respuestas_string = respuestas_usuario.respuestas.strip()
    respuestas_lista = respuestas_string.split(",")
    
    print(f"Respuestas del usuario: {respuestas_lista}")
    
    # Verificar que el número de respuestas coincida con el número de preguntas
    if len(respuestas_lista) != len(preguntas):
        raise HTTPException(
            status_code=400, 
            detail=f"El número de respuestas ({len(respuestas_lista)}) no coincide con el número de preguntas ({len(preguntas)})"
        )

    respuestas_correctas = 0

    # Compara las respuestas
    for i, pregunta in enumerate(preguntas):
        respuesta_usuario_str = respuestas_lista[i].strip().upper()
        # Convertir "SI" a True y "NO" a False
        # Convertir la respuesta correcta de la BD a mayúsculas para comparar
        respuesta_correcta_str = pregunta.resp_correcta.strip().upper()
        
        #print(f"Pregunta {pregunta.id_pregunta}: Usuario respondió '{respuesta_usuario_str}' ({respuesta_usuario_bool}), Correcta: {pregunta.resp_correcta}")
        print(f"\n--- Pregunta {i+1} (ID: {pregunta.id_pregunta}) ---")
        print(f"Texto: {pregunta.contenido}")
        print(f"Respuesta correcta: {respuesta_correcta_str}")
        print(f"Usuario respondió: '{respuesta_usuario_str}'")
        print(f"¿Es correcta?: {'✓' if respuesta_usuario_str == respuesta_correcta_str else '✗'}")

        if respuesta_usuario_str == respuesta_correcta_str:
            respuestas_correctas += 1

    # Actualizamos el campo 'estrella' en la tabla 'control'
    control = db.query(Control).filter(Control.id_usuario == id_usuario, Control.id_cuento == id_cuento).first()

    if control:
        control.estrella = respuestas_correctas
    else:
        control = Control(id_usuario=id_usuario, id_cuento=id_cuento, estrella=respuestas_correctas)
        db.add(control)

    db.commit()

    return {
        "message": "Respuestas enviadas y comparadas exitosamente",
        "status": 200,
        "data": {"respuestas_correctas": respuestas_correctas}
    }
