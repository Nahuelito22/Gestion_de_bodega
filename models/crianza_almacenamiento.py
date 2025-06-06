import uuid
from datetime import datetime
from models.db import db
from sqlalchemy import Enum
from .estados.estado_crianza import EstadoCrianza

class CrianzaAlmacenamiento(db.Model):
    __tablename__ = 'crianza_almacenamiento'

    # FK a loteVino (la columna en la tabla que apunta a la clave primaria de loteVino)
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    lote_vino_id = db.Column(db.String(36), db.ForeignKey('lote_vino.id'), nullable=False)

    # Fechas de inicio y fin de crianza
    fecha_inicio = db.Column(db.DateTime, nullable=False)
    fecha_fin = db.Column(db.DateTime, nullable=True)

    # Parametros de control
    tipo_recipiente = db.Column(db.String(100), nullable=True)
    volumen_litros = db.Column(db.Float, nullable=True)
    ph_medicion = db.Column(db.Float, nullable=True)
    acidez_medicion_g_l = db.Column(db.Float, nullable=True)
    notas = db.Column(db.String(300), nullable=True)

    estado=db.Column(
        Enum(EstadoCrianza, name='estado_fermentacion_enum'),
        nullable=False,
        default=EstadoCrianza.otros
    )

    # Relación para poder acceder al objeto LoteVino desde un FermentacionAlcoholica
    lote_vino = db.relationship('LoteVino', backref=db.backref('crianzas', lazy=True))

    def __repr__(self):
        return f"<CrianzaAlmacenamiento {self.id} - Lote {self.lote_vino_id}>"
