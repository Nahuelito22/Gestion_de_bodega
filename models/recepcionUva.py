import uuid
from datetime import datetime
from models.db import db

class RecepcionUva(db.Model):
    __tablename__ = 'recepcion_uva'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))

    # FK a loteVino (la columna en la tabla que apunta a la clave primaria de loteVino)
    lote_vino_id = db.Column(db.String(36), db.ForeignKey('lote_vino.id'), nullable=False)

    fecha_recepcion = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    cantidad_kg = db.Column(db.Float, nullable=False)
    ph = db.Column(db.Float, nullable=True)
    acidez_total_g_l = db.Column(db.Float, nullable=True)
    azucar_brix = db.Column(db.Float, nullable=True)
    notas = db.Column(db.String(300), nullable=True)

    # Relación para poder acceder al objeto LoteVino desde un recepcionUva
    lote_vino = db.relationship('LoteVino', backref=db.backref('recepciones', lazy=True))

    def __repr__(self):
        return f"<RecepcionUva {self.id} - Lote {self.lote_vino_id}>"
