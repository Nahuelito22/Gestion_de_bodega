import uuid
from flask import Blueprint, request, jsonify
from datetime import datetime
from models.RecepcionUva import RecepcionUva
from models.db import db

# Creamos el blueprint para recepcionUva
recepcionUva_bp = Blueprint('recepcionUva_bp', __name__)

#GET / Obtener las recepciones de uva

recepcionUva_bp.route('/', methods=['GET'])
def get_recepcionesUva():
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

# GET / Obtener Recepcion por ID


recepcionUva_bp.route('/<string:id>', methods=['GET'] )
def get_recepcion(id):
    recepcion=RecepcionUva.query.get(id)
    if not recepcion:
        return jsonify ({'error': 'recepcion no encontrada'}), 404
    return jsonify({
        'id':recepcion.id,
        'lote_vino_id':recepcion.lote_vino_id,
        'fecha_recepcion': recepcion.fecha_recepcion.isoformat(),            'cantidad_kg':recepcion.cantidad_kg,
        'ph':recepcion.ph,
        'acidez_total_g_l':recepcion.acidez_total_g_l,
        'azucar_brix':recepcion.azucar_brix,
        'notas':recepcion.notas
    }),200

recepcionUva_bp.route('/', methods=['POST'])
def crea_recepcion():
    data = request.get_json()

    # Validar algunos campos
    if not data or 'cantidad_kg' not in data or 'fecha_recepcion' not in data or 'ph' not in data:
        return jsonify ({'error': 'faltan campos requeridos'}),400
    try:
        fecha_recepcion = datetime.fromisoformat(data['fecha_recepcion'])  # conversión importante
    except ValueError:
        return jsonify({'error': 'Formato de fecha inválido'}), 400
    
    nueva_recepcion= RecepcionUva(
        lote_vino_id=data['lote_vino_id'],
        fecha_recepcion=data ['fecha_recepcion'],
        cantidad_kg= data ['cantidad_kg'],
        ph= data['ph'],
        acidez_total_g_l= data ['acidez_total_g_l'],
        azucar_brix=data['azucar_brix'],
        notas= data['notas'],
    )

    db.session.add(nueva_recepcion)
    db.session.commit()

    return jsonify({
        'id': nueva_recepcion.id,
        'lote_vino_id':nueva_recepcion.lote_vino_id,
        'fecha_recepcion': nueva_recepcion.fecha_recepcion,
        'cantidad_kg':nueva_recepcion.cantidad_kg.isoformat(),
        'ph':nueva_recepcion.ph,
        'acidez_total_g_l': nueva_recepcion.acidez_total_g_l,
        'azucar_brix': nueva_recepcion.azucar_brix,
        'notas':nueva_recepcion.notas
    
    }), 201