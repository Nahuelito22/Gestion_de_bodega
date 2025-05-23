import uuid
from datetime import datetime
from models.db import db

class Embotellado(db.Model):
    __tablename__ = 'embotellado'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    
    # FK a loteVino (la columna en la tabla que apunta a la clave primaria de loteVino)
    lote_vino_id = db.Column(db.String(36), db.ForeignKey('lote_vino.id'), nullable=False)

    # Fecha para control
    fecha_embotellado = db.Column(db.DateTime, nullable=False)
    
    # Parametros de control y seguimiento finales
    numero_botellas_producidas = db.Column(db.Integer, nullable=True)
    volumen_por_botella_ml = db.Column(db.Float, nullable=True)
    ph_final = db.Column(db.Float, nullable=True)
    acidez_final_g_l = db.Column(db.Float, nullable=True)
    grado_alcoholico_final_porcentaje = db.Column(db.Float, nullable=True)
    
    #Notas para observaciones
    notas = db.Column(db.String(300), nullable=True)

    # Relación para poder acceder al objeto LoteVino desde un recepcionUva
    lote_vino = db.relationship('LoteVino', backref=db.backref('embotellados', lazy=True))

    def __repr__(self):
        return f"<Embotellado {self.id} - Lote {self.lote_vino_id}>"
