from datetime import datetime
import uuid
from flask import Blueprint, request, jsonify
from models.embotellado import Embotellado  # importamos el modelo
from models.db import db

# Creamos el blueprint para recepcionUva
embotellado_bp = Blueprint('embotellado_bp', __name__)

@embotellado_bp.route('/', methods=['GET'])
def get_embotellamientos():
    embotellamientos= Embotellado.query.all()
    resultados = []

    for res in embotellamientos:
        resultados.append({
            'id':res.id,
            'lote_vino_id' : res.lote_vino_id,
            'fecha_embotellado':res.fecha_embotellado,
            'numero_botellas_producidas':res.numero_botellas_producidas,
            'volumen_por_botella_ml':res.volumen_por_botella_ml,
            'ph_final':res.ph_final,
            'acidez_final_g_l':res.acidez_final_g_l,
            'grado_alcoholico_final_porcentaje':res.grado_alcoholico_final_porcentaje,
            'notas':res.notas
        })
    return jsonify(resultados),200

@embotellado_bp.route('/<string:id>', methods=['GET'])
def get_embotellamiento(id):
    res= Embotellado.query.get(id)

    if not res:
        return jsonify ({'error': 'Embotellamiento no encontrado'})

    return jsonify ({
        'id':res.id,
        'lote_vino_id' : res.lote_vino_id,
        'fecha_embotellado':res.fecha_embotellado,
        'numero_botellas_producidas':res.numero_botellas_producidas,
        'volumen_por_botella_ml':res.volumen_por_botella_ml,
        'ph_final':res.ph_final,
        'acidez_final_g_l':res.acidez_final_g_l,
        'grado_alcoholico_final_porcentaje':res.grado_alcoholico_final_porcentaje,
        'notas':res.notas
    }),200


@embotellado_bp.route('/', methods=['POST'])
def crear_embotellamiento ():
    data=request.get_json()

    #validamos

    if not data or 'lote_vino_id' not in data or 'fecha_embotellado' not in data or 'numero_botellas_producidas' not in data or 'volumen_por_botella_ml' not in data or 'ph_final' not in data or 'acidez_final_g_l' not in data or 'grado_alcoholico_final_porcentaje' not in data:
        return jsonify ({'Error': 'Faltan campos requeridos'}),400
    try:
        fecha_embotellamiento= datetime.fromisoformat(data['fecha_embotellado']) # conversión importante
    except ValueError:
        return jsonify({'error': 'Formato de fecha inválido'}), 400
    nuevo_embotellamiento = Embotellado(
        lote_vino_id=data['lote_vino_id'],
        fecha_embotellado=fecha_embotellamiento,
        numero_botellas_producidas=data['numero_botellas_producidas'],
        volumen_por_botella_ml=data['volumen_por_botella_ml'],
        ph_final=data['ph_final'],
        acidez_final_g_l=data['acidez_final_g_l'],
        grado_alcoholico_final_porcentaje=data['grado_alcoholico_final_porcentaje'],
        notas=data.get('notas')  # devuelve None si no está
    )
    db.session.add(nuevo_embotellamiento)
    db.session.commit()

    return jsonify({
        'id':nuevo_embotellamiento.id,
        'lote_vino_id' : nuevo_embotellamiento.lote_vino_id,
        'fecha_embotellado':nuevo_embotellamiento.fecha_embotellado.isoformat(),
        'numero_botellas_producidas':nuevo_embotellamiento.numero_botellas_producidas,
        'volumen_por_botella_ml':nuevo_embotellamiento.volumen_por_botella_ml,
        'ph_final':nuevo_embotellamiento.ph_final,
        'acidez_final_g_l':nuevo_embotellamiento.acidez_final_g_l,
        'grado_alcoholico_final_porcentaje':nuevo_embotellamiento.grado_alcoholico_final_porcentaje,
        'notas':nuevo_embotellamiento.notas
    }),201

@embotellado_bp.route('/<string:id>', methods=['PATCH'])
def modificar_embotellado(id):
    cambio_embotellado=Embotellado.query.get(id)
    if not cambio_embotellado:
        return jsonify ({'error': ' embotellado no encontrado'}),404
    
    data=request.get_json()
    if not data:
        return({'error': ' no hay datos para actualizar'}),400
    try:
        if 'fecha_embotellado' in data:
            cambio_embotellado.fecha_embotellado = datetime.fromisoformat(data['fecha_embotellado'])

    except ValueError:
        return jsonify({'error': 'Formato de fecha inválido'}), 400
    if 'numero_botellas_producidas' in data:
        cambio_embotellado.numero_botellas_producidas=data['numero_botellas_producidas']
    if 'volumen_por_botella_ml' in data:
        cambio_embotellado.volumen_por_botella_ml=data['volumen_por_botella_ml']
    if 'ph_final' in data:
        cambio_embotellado.ph_final=data['ph_final']
    if 'acidez_final_g_l' in data:
        cambio_embotellado.acidez_final_g_l=data['acidez_final_g_l']
    if 'grado_alcoholico_final_porcentaje' in data:
        cambio_embotellado.grado_alcoholico_final_porcentaje=data['grado_alcoholico_final_porcentaje']
    if 'notas' in data:
        cambio_embotellado.notas=data['notas']

    db.session.commit()
    return jsonify({
        'id':cambio_embotellado.id,
        'lote_vino_id' : cambio_embotellado.lote_vino_id,
        'fecha_embotellado':cambio_embotellado.fecha_embotellado.isoformat(),
        'numero_botellas_producidas':cambio_embotellado.numero_botellas_producidas,
        'volumen_por_botella_ml':cambio_embotellado.volumen_por_botella_ml,
        'ph_final':cambio_embotellado.ph_final,
        'acidez_final_g_l':cambio_embotellado.acidez_final_g_l,
        'grado_alcoholico_final_porcentaje':cambio_embotellado.grado_alcoholico_final_porcentaje,
        'notas':cambio_embotellado.notas
    }),200