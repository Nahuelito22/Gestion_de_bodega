from datetime import datetime
import uuid
from flask import Blueprint, request, jsonify
from models.crianza_almacenamiento import CrianzaAlmacenamiento  # importamos el modelo
from models.db import db

# Creamos el blueprint para recepcionUva
crianza_bp = Blueprint('crianza_bp', __name__)
#GET
@crianza_bp.route('/', methods=['GET'])
def get_almacenamientos():
    almacenamientos=CrianzaAlmacenamiento.query.all()
    resultados=[]

    for res in almacenamientos:
        resultados.append({
            'id':res.id,
            'lote_vino_id' : res.lote_vino_id,
            'fecha_inicio':res.fecha_inicio,
            'fecha_fin': res.fecha_fin,
            'tipo_recipiente':res.tipo_recipiente,
            'volumen_litros':res.volumen_litros,
            'ph_medicion':res.ph_medicion,
            'acidez_medicion_g_l':res.acidez_medicion_g_l,
            'notas':res.notas
        })
    return jsonify(resultados),200
#GET by ID
@crianza_bp.route('/<string:id>', methods=['GET'])
def get_almacenamiento(id):
    res=CrianzaAlmacenamiento.query.get(id)
    if not res:
        return jsonify({'error': 'Crianza/Almacenamiento no encontrado'})
    return jsonify({
        'id':res.id,
        'lote_vino_id' : res.lote_vino_id,
        'fecha_inicio':res.fecha_inicio,
        'fecha_fin': res.fecha_fin,
        'tipo_recipiente':res.tipo_recipiente,
        'volumen_litros':res.volumen_litros,
        'ph_medicion':res.ph_medicion,
        'acidez_medicion_g_l':res.acidez_medicion_g_l,
        'notas':res.notas
    }),201

@crianza_bp.route('/', methods=['POST'])
def crear_almacenamiento():
    
    data= request.get_json()
    # validaciones
    if not data or "lote_vino_id" not in data or "fecha_inicio" not in data or "fecha_fin" not in data or "tipo_recipiente" not in data or "volumen_litros" not in data or "acidez_medicion_g_l" not in data or "ph_medicion" not in data:
        return jsonify ({'Error': 'Faltan campos requeridos'}),400
    try:
        fecha_recepcion = datetime.fromisoformat(data['fecha_inicio']) 
        fecha_final= datetime.fromisoformat(data['fecha_fin']) # conversión importante
    except ValueError:
        return jsonify({'error': 'Formato de fecha inválido'}), 400
    
    nuevo_almacenamiento= CrianzaAlmacenamiento(
        lote_vino_id=data['lote_vino_id'],
        fecha_inicio=fecha_recepcion,
        fecha_fin= fecha_final,
        tipo_recipiente=data['tipo_recipiente'],
        volumen_litros=data['volumen_litros'],
        ph_medicion=data['ph_medicion'],
        acidez_medicion_g_l=data['acidez_medicion_g_l'],
        notas=data.get('notas')  # devuelve None si no está
    )

    db.session.add(nuevo_almacenamiento)
    db.session.commit()

    # Devolver respuesta con los datos recién creados
    return jsonify({
        'id': nuevo_almacenamiento.id,
        'lote_vino_id': nuevo_almacenamiento.lote_vino_id,
        'fecha_inicio': nuevo_almacenamiento.fecha_inicio.isoformat(),
        'fecha_fin': nuevo_almacenamiento.fecha_fin.isoformat(),
        'tipo_recipiente': nuevo_almacenamiento.tipo_recipiente,
        'volumen_litros': nuevo_almacenamiento.volumen_litros,
        'ph_medicion': nuevo_almacenamiento.ph_medicion,
        'acidez_medicion_g_l': nuevo_almacenamiento.acidez_medicion_g_l,
        'notas': nuevo_almacenamiento.notas
    }), 201

@crianza_bp.route('/<string:id>', methods=['PATCH'])
def modificar_almacenamiento(id):
    almacenamiento_cambio= CrianzaAlmacenamiento.query.get(id)
    if not almacenamiento_cambio:
        return jsonify({'error': ' Crianza/Almacenamiento no encontrado'}),404

    data= request.get_json()
    if not data:
        return({'error': 'no hay datos para actualizar'}),400

    try:
        if 'fecha_inicio' in data:
            almacenamiento_cambio.fecha_inicio = datetime.fromisoformat(data['fecha_inicio'])
        if 'fecha_fin' in data:
            almacenamiento_cambio.fecha_fin = datetime.fromisoformat(data['fecha_fin'])
    except ValueError:
        return jsonify({'error': 'Formato de fecha inválido'}), 400
    
    if 'tipo_recipiente' in data:
        almacenamiento_cambio.tipo_recipiente=data['tipo_recipiente']
    if 'volumen_litros' in data:
        almacenamiento_cambio.volumen_litros=data['volumen_litros']
    if 'ph_medicion' in data:
        almacenamiento_cambio.ph_medicion=data['ph_medicion']
    if 'acidez_medicion_g_l' in data:
        almacenamiento_cambio.acidez_medicion_g_l=data['acidez_medicion_g_l']
    if 'notas' in data:
        almacenamiento_cambio.notas=data['notas']

    db.session.commit()
    return jsonify({
        'id': almacenamiento_cambio.id,
        'lote_vino_id': almacenamiento_cambio.lote_vino_id,
        'fecha_inicio': almacenamiento_cambio.fecha_inicio.isoformat(),
        'fecha_fin': almacenamiento_cambio.fecha_fin.isoformat(),
        'tipo_recipiente': almacenamiento_cambio.tipo_recipiente,
        'volumen_litros': almacenamiento_cambio.volumen_litros,
        'ph_medicion': almacenamiento_cambio.ph_medicion,
        'acidez_medicion_g_l': almacenamiento_cambio.acidez_medicion_g_l,
        'notas': almacenamiento_cambio.notas
    }), 201