import uuid
from flask import Blueprint, request, jsonify
from models.fermentacionAlcoholica import FermentacionAlcoholica  # importamos el modelo
from datetime import datetime
from models.db import db

# Creamos el blueprint para recepcionUva
fermentacion_bp = Blueprint('fermentacion_bp', __name__)

@fermentacion_bp.route('/' , methods=['GET'])
def get_fermentaciones():
    fermentaciones=FermentacionAlcoholica.query.all() #traemos todas las fermentaciones
    resultados=[] 
    for res in fermentaciones:
        resultados.append({
            'id':res.id,
            'lote_vino_id' : res.lote_vino_id,
            'fecha_inicio':res.fecha_inicio,
            'fecha_fin': res.fecha_fin,
            'temperatura_control_c':res.temperatura_control_c,
            'densidad_inicial':res.densidad_inicial,
            'densidad_final':res.densidad_final,
            'ph_medicion':res.ph_medicion,
            'acidez_volatil_g_l':res.acidez_volatil_g_l,
            'tipo_levadura':res.tipo_levadura,
            'notas':res.notas

        })
    return jsonify(resultados),200




@fermentacion_bp.route('/<string:id>', methods=['GET'] )
def get_fermentacion(id):
    res=FermentacionAlcoholica.query.get(id)
    if not res:
        return jsonify ({'error': 'fermentacion no encontrada'}), 404
    return jsonify({
        'id':res.id,
        'lote_vino_id' : res.lote_vino_id,
        'fecha_inicio':res.fecha_inicio.isoformat(),
        'fecha_fin': res.fecha_fin.isoformat(),
        'temperatura_control_c':res.temperatura_control_c,            'densidad_inicial':res.densidad_inicial,
        'densidad_final':res.densidad_final,
        'ph_medicion':res.ph_medicion,
        'acidez_volatil_g_l':res.acidez_volatil_g_l,
        'tipo_levadura':res.tipo_levadura,
        'notas':res.notas
    }),200