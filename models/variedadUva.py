import uuid
from models.db import db

class VariedadUva(db.Model):
    __tablename__ = 'variedades_de_uva'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))#uuid especifico de cada Variedad
    nombre= db.Column (db.String(40), unique=True, nullable=False)    
    origen= db.Column (db.String(30), nullable=False)
    imagen= db.Column (db.String(255), nullable=True)

    def __init__(self, nombre, origen, imagen=None):
        self.nombre = nombre
        self.origen= origen
        self.imagen=imagen
    

    def serialize(self):
        return {
            'id': self.id,
            'nombre':self.nombre,
            'origen':self.origen,
            'imagen':self.imagen
        }