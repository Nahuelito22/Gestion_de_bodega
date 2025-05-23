import uuid
from datetime import datetime
from models.db import db

class RecepcionUva(db.Model):
    __tablename__ = 'recepcion_uva'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    
    # ForeignKey a LoteVino.id (cadena UUID)
    lote_vino_id = db.Column(db.String(36), db.ForeignKey('lote_vino.id'), nullable=False)

    fecha_recepcion = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    cantidad_kilos = db.Column(db.Float, nullable=False)
    proveedor = db.Column(db.String(150), nullable=True)
    observaciones = db.Column(db.String(300), nullable=True)

    # Relación para poder acceder al lote desde la recepción
    lote_vino = db.relationship('LoteVino', backref=db.backref('recepciones', lazy=True))

    def __repr__(self):
        return f"<RecepcionUva {self.id} - Lote {self.lote_vino_id} - {self.cantidad_kilos}kg>"
