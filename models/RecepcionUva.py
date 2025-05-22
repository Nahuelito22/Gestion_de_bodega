import uuid
from models.db import db

class RecepcionUva(db.Model):
    __tablename__ = 'recepcion_de_uva'
    id= db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    lote=db.Column(db.String(25), nullable=False, unique=True)
    fecha_ingreso=db.Column(db.Date, nullable=False)
    cantidad=db.Column(db.Float, nullable=False)
    observacion = db.Column(db.String(80), nullable=True)
    variedad_id=db.Column(db.String(36), db.ForeignKey('variedades_de_uva.id'), nullable=False)
    variedad= db.relationship('VariedadDeUva', backref='recepciones')

    def __init__(self, lote, fecha_ingreso, cantidad, observacion, variedad_id):
        self.lote=lote
        self.fecha_ingreso=fecha_ingreso
        self.cantidad=cantidad
        self.observacion=observacion
        self.variedad_id=variedad_id

    def serialize(self):
        return{
            'id':self.id,
            'lote':self.lote,
            'fecha_ingreso':self.fecha_ingreso.isoformat() if self.fecha_ingreso else None,
            'cantidad':self.cantidad,
            'observacion':self.observacion,
            'variedad_id':self.variedad_id
        }