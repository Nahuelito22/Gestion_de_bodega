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

@fermentacion_bp.route('/', methods=['POST'])
def crear_fermentacion():
    data= request.get_json()

    #algunas validaciones
    if not data or "lote_vino_id" not in data or "fecha_inicio" not in data or "fecha_fin" not in data or "temperatura_control_c" not in data or "densidad_inicial" not in data or "densidad_final" not in data or "ph_medicion" not in data or "acidez_volatil_g_l" not in data or "tipo_levadura" not in data:
        return jsonify ({'Error': 'Faltan campos requeridos'}),400
    
    try:
        fecha_recepcion = datetime.fromisoformat(data['fecha_inicio']) 
        fecha_final= datetime.fromisoformat(data['fecha_fin']) # conversión importante
    except ValueError:
        return jsonify({'error': 'Formato de fecha inválido'}), 400
    
    nueva_fermentacion= FermentacionAlcoholica(
        lote_vino_id=data['lote_vino_id'],
        fecha_inicio=fecha_recepcion,
        fecha_fin= fecha_final,
        temperatura_control_c=data['temperatura_control_c'],
        densidad_inicial=data['densidad_inicial'],
        densidad_final=data['densidad_final'],
        ph_medicion=data['ph_medicion'],
        acidez_volatil_g_l=data['acidez_volatil_g_l'],
        tipo_levadura=data['tipo_levadura'],
        notas=data.get('notas')  # devuelve None si no está
    )

    db.session.add(nueva_fermentacion)
    db.session.commit()

    return jsonify({
        'id':nueva_fermentacion.id,
        'lote_vino_id' : nueva_fermentacion.lote_vino_id,
        'fecha_inicio':nueva_fermentacion.fecha_inicio.isoformat(),
        'fecha_fin': nueva_fermentacion.fecha_fin.isoformat(),
        'temperatura_control_c':nueva_fermentacion.temperatura_control_c,            
        'densidad_inicial':nueva_fermentacion.densidad_inicial,
        'densidad_final':nueva_fermentacion.densidad_final,
        'ph_medicion':nueva_fermentacion.ph_medicion,
        'acidez_volatil_g_l':nueva_fermentacion.acidez_volatil_g_l,
        'tipo_levadura':nueva_fermentacion.tipo_levadura,
        'notas':nueva_fermentacion.notas
    }),201


@fermentacion_bp.route('/<string:id>', methods=['PATCH'])
def modificar_fermentacion(id):
    fermentacion_cambio=FermentacionAlcoholica.query.get(id)
    if not fermentacion_cambio:
        return jsonify({'error': 'Fermentacion no encontrada'}),404

    data=request.get_json()
    if not data:
        return ({'error' : ' no hay datos para actualizar'}),400

    #validamos datos para ir actualizando

     # Validamos y actualizamos campos individualmente
    try:
        if 'fecha_inicio' in data:
            fermentacion_cambio.fecha_inicio = datetime.fromisoformat(data['fecha_inicio'])
        if 'fecha_fin' in data:
            fermentacion_cambio.fecha_fin = datetime.fromisoformat(data['fecha_fin'])
    except ValueError:
        return jsonify({'error': 'Formato de fecha inválido'}), 400

    if 'temperatura_control_c' in data:
        fermentacion_cambio.temperatura_control_c=data['temperatura_control_c']
    if 'densidad_inicial' in data:
        fermentacion_cambio.densidad_inicial=data['densidad_inicial']
    if 'densidad_final' in data:
        fermentacion_cambio.densidad_final= data['densidad_final']
    if 'ph_medicion' in data:
        fermentacion_cambio.ph_medicion=data['ph_medicion']
    if 'acidez_volatil_g_l' in data:
        fermentacion_cambio.acidez_volatil_g_l=data['acidez_volatil_g_l']
    if 'tipo_levadura' in data:
        fermentacion_cambio.tipo_levadura=data['tipo_levadura']
    if 'notas' in data:
        fermentacion_cambio.notas=data['notas']

    db.session.commit()

    return jsonify({
        'id':fermentacion_cambio.id,
        'lote_vino_id' : fermentacion_cambio.lote_vino_id,
        'fecha_inicio':fermentacion_cambio.fecha_inicio.isoformat(),
        'fecha_fin': fermentacion_cambio.fecha_fin.isoformat(),
        'temperatura_control_c':fermentacion_cambio.temperatura_control_c,            
        'densidad_inicial':fermentacion_cambio.densidad_inicial,
        'densidad_final':fermentacion_cambio.densidad_final,
        'ph_medicion':fermentacion_cambio.ph_medicion,
        'acidez_volatil_g_l':fermentacion_cambio.acidez_volatil_g_l,
        'tipo_levadura':fermentacion_cambio.tipo_levadura,
        'notas':fermentacion_cambio.notas

    }),200