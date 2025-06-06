import uuid
from datetime import datetime
from sqlalchemy import Enum
from models.db import db
from .estados.estado_fermentacion import EstadoFermentacion

class FermentacionAlcoholica(db.Model):
    __tablename__ = 'fermentacion_alcoholica'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    
    # FK a loteVino (la columna en la tabla que apunta a la clave primaria de loteVino)
    lote_vino_id = db.Column(db.String(36), db.ForeignKey('lote_vino.id'), nullable=False)

    # Fechas de inicio y fin de fermentacion
    fecha_inicio = db.Column(db.DateTime, nullable=False)
    fecha_fin = db.Column(db.DateTime, nullable=True)

    # Parametros del control de la fermentacion
    temperatura_control_c = db.Column(db.Float, nullable=True)
    densidad_inicial = db.Column(db.Float, nullable=True)
    densidad_final = db.Column(db.Float, nullable=True)
    ph_medicion = db.Column(db.Float, nullable=True)
    acidez_volatil_g_l = db.Column(db.Float, nullable=True)
    tipo_levadura = db.Column(db.String(100), nullable=True)
    notas = db.Column(db.String(300), nullable=True)
    estado=db.Column(
        Enum(EstadoFermentacion, name='estado_fermentacion_enum'),
        nullable=False,
        default=EstadoFermentacion.en_proceso
    )
    # Relación para poder acceder al objeto LoteVino desde un FermentacionAlcoholica
    lote_vino = db.relationship('LoteVino', backref=db.backref('fermentaciones', lazy=True))

    def __repr__(self):
        return f"<FermentacionAlcoholica {self.id} - Lote {self.lote_vino_id}>"
