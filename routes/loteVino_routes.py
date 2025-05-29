from datetime import datetime
import uuid
from flask import Blueprint, request, jsonify
from models.loteVino import LoteVino  # importamos el modelo
from models.db import db

# Creamos el blueprint para LoteVino
loteVino_bp = Blueprint('loteVino_bp', __name__)

@loteVino_bp.route('/', methods=['GET'])
def get_lotes():
    lotes=LoteVino.query.all()
    resultados=[]

    for res in lotes:
        resultados.append({
            'id':res.id,
            'nombre_identificativo':res.nombre_identificativo,
            'fecha_creacion':res.fecha_creacion,
            'variedad_uva_id':res.variedad_uva_id
        })
    return jsonify(resultados),200

@loteVino_bp.route('/<string:id>', methods=['GET'])
def get_lote(id):
    res= LoteVino.query.get(id)
    if not res:
        return jsonify({'error': 'Lote no encontrado'}),404
    return jsonify({
        'id':res.id,
        'nombre_identificativo':res.nombre_identificativo,
        'fecha_creacion':res.fecha_creacion,
        'variedad_uva_id':res.variedad_uva_id
    }),200

@loteVino_bp.route('/', methods=['POST'])
def crear_lote():
    data= request.get_json()

    if not data or 'nombre_identificativo' not in data or 'fecha_creacion' not in data or 'variedad_uva_id' not in data:
        return ({'error': ' faltan campos requeridos'}),400
    try:
        fecha_creacion_lote=datetime.fromisoformat(data['fecha_creacion']) 
    except ValueError:
        return jsonify({'error': ' formato de fecha invalido'}),400

    nuevo_lote= LoteVino(
        nombre_identificativo=data['nombre_identificativo'],
        fecha_creacion=fecha_creacion_lote,
        variedad_uva_id=data['variedad_uva_id']
    )

    db.session.add(nuevo_lote)
    db.session.commit()

    return jsonify({
        'id':nuevo_lote.id,
        'nombre_identificativo':nuevo_lote.nombre_identificativo,
        'fecha_creacion':nuevo_lote.fecha_creacion,
        'variedad_uva_id':nuevo_lote.variedad_uva_id

    }),201



@loteVino_bp.route('/<string:id>', methods=['PATCH'])
def modificar_lote(id):
    cambio_lote=LoteVino.query.get(id)
    if not cambio_lote:
        return jsonify({'error': ' no se encuentra el lote'}),404

    data= request.get_json()

    if not data:
        return jsonify ({'error': ' no hay datos para actualizar'}),400
    
    try:
        if 'fecha_creacion' in data:
            cambio_lote.fecha_creacion= datetime.fromisoformat(data['fecha_creacion'])
    except ValueError:
        return jsonify({'error': 'formato de fecha invalido'}),400
    
    if 'nombre_identificativo' in data:
        cambio_lote.nombre_identificativo=data['nombre_identificativo']
    if 'variedad_uva_id' in data:
        cambio_lote.variedad_uva_id=data['variedad_uva_id']

    db.session.commit()
    return jsonify({
        'id':cambio_lote.id,
        'nombre_identificativo':cambio_lote.nombre_identificativo,
        'fecha_creacion':cambio_lote.fecha_creacion.isoformat(),
        'variedad_uva_id':cambio_lote.variedad_uva_id
    }),200