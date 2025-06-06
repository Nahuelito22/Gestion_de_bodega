import enum

class EstadoLote(enum.Enum):
    activo= "Activo"
    finalizado="Finalizado"
    en_proceso="En_proceso"
    cancelado="Cancelado"
    detenido="Detenido / Pausado"