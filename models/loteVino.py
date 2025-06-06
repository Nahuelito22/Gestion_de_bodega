import uuid
from datetime import datetime
from models.db import db
from models.variedadUva import VariedadUva  # Importamos para la relación
from sqlalchemy import Enum
from .estados.estado_lote import EstadoLote
class LoteVino(db.Model):
    __tablename__ = 'lote_vino'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    nombre_identificativo = db.Column(db.String(100), nullable=False)
    fecha_creacion = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    # FK a VariedadUva (la columna en la tabla que apunta a la clave primaria de VariedadUva)
    variedad_uva_id = db.Column(db.String(36), db.ForeignKey('variedad_uva.id'), nullable=False)

    # Relación para poder acceder al objeto VariedadUva desde un LoteVino
    variedad_uva = db.relationship('VariedadUva', backref=db.backref('lotes_vino', lazy='dynamic'))
    estado= db.Column(
        Enum(EstadoLote, name='estado_lote_enum'),
        nullable=False,
        default=EstadoLote.activo
    )

    def __repr__(self):
        return f"<LoteVino {self.nombre_identificativo} (id={self.id}) - Variedad: {self.variedad_uva.nombre}>"
