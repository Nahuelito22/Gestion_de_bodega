import uuid
from flask import Blueprint, request, jsonify
from models.RecepcionUva import RecepcionUva
from models.db import db

# Creamos el blueprint para recepcionUva
recepcionUva_bp = Blueprint('recepcionUva_bp', __name__)

#GET / Obtener las recepciones de uva

recepcionUva_bp.route('/', methods=['GET'])
def get_recepcionUva():
    recepciones=RecepcionUva.query.all() #Traemos todas las Recepciones
    resultados= []
    for r in recepciones:
        resultados.append({
            'id':r.id,
            'lote_vino_id':r.lote_vino_id,
            'fecha_recepcion': r.fecha_recepcion.isoformat(),
            'cantidad_kg':r.cantidad_kg,
            'ph':r.ph,
            'acidez_total_g_l':r.acidez_total_g_l,
            'azucar_brix':r.azucar_brix,
            'notas':r.notas

        })
    return jsonify(resultados), 200
