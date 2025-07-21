from sqlalchemy import Column, Integer, String, Boolean
from database import Base

class Pregunta(Base):
    __tablename__ = 'pregunta'

    id_pregunta = Column(Integer, primary_key=True, index=True)
    id_cuento = Column(Integer)  # Relación con el cuento
    contenido = Column(String)
    resp_correcta = Column(Boolean)  # Cambiar de String a Boolean

    #resp_correcta = Column(String)  # Almacena si la respuesta es correcta (sí/no)