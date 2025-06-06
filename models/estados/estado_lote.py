import enum

class EstadoLote(enum.Enum):
    activo= "activo"
    finalizado="finalizado"
    en_proceso="en_proceso"
    cancelado="cancelado"
    detenido="detenido"