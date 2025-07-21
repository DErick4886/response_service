from sqlalchemy import Column, Integer
from database import Base

class Control(Base):
    __tablename__ = 'control'

    id_control = Column(Integer, primary_key=True, index=True)
    id_usuario = Column(Integer)
    id_cuento = Column(Integer)
    estrella = Column(Integer)  # Almacena el número de respuestas correctas
