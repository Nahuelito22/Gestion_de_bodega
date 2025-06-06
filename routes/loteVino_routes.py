from datetime import datetime
import uuid
from flask import Blueprint, flash, redirect, render_template, request, jsonify, url_for
from models.loteVino import LoteVino  # importamos el modelo
from models.db import db
from models.variedadUva import VariedadUva
from flask_login import login_required
from models.estados.estado_lote import EstadoLote

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
def añadir_lote():
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

#metodo para renderizar el formulario de html
@loteVino_bp.route('/crear', methods=['GET'])
@login_required
def mostrar_formulario_crear_lote():
    variedades = VariedadUva.query.all()
    estados = list(EstadoLote)  # Esto te da [EstadoLote.activo, EstadoLote.finalizado, ...]

    return render_template('lotes/crear_lote.html', variedades= variedades , estados=estados) 

@loteVino_bp.route('/crear_lote', methods = ['POST'])
@login_required
def crear_lote():
    nombre_identificatorio= request.form['nombre_identificativo']
    variedad_uva_id = request.form['variedad_uva_id']
    estado=request.form['estado']
    estado_enum=EstadoLote[estado]

    nuevo_lote = LoteVino(
        nombre_identificativo=nombre_identificatorio,
        variedad_uva_id=variedad_uva_id,
        estado=estado_enum
    )

    db.session.add(nuevo_lote)
    db.session.commit()

    flash('Lote creado correctamente.', 'success')
    return redirect(url_for('loteVino_bp.listar_lotes'))  # redirigí a donde muestres los lotes



@loteVino_bp.route('/listar', methods=['GET']) # Puse '/listar' como ejemplo de URL
@login_required
def listar_lotes():
    # Obtener todas las variedades de uva de la base de datos como objetos VariedadUva
    estado=request.args.get('estado')
    if estado:
        try:
            estado_enum=EstadoLote[estado]
        except KeyError:
            estado_enum=None
    else:
        estado_enum=None
    
    lotes = LoteVino.query.all()

    
    # Renderiza la plantilla 'variedades.html' y pasa la lista de objetos 'lotes'
    return render_template('/lotes/listar_lotes.html', lotes=lotes, estado=estado_enum), 200


@loteVino_bp.route('/menu', methods=['GET'])
@login_required
def menu_variedades():
    return render_template('lotes/lotes_menu.html')


@loteVino_bp.route('/editar_lote/<string:id>', methods=['GET', 'POST'])
@login_required
def editar_lote(id):
    lote = LoteVino.query.get_or_404(id)
    variedades = VariedadUva.query.all()


    if request.method == 'POST':
        lote.nombre_identificativo = request.form['nombre_identificativo']
        #lote.fecha_creacion = request.form['fecha_creacion']

        try:
            lote.variedad_uva_id = request.form['variedad_uva_id']
            #asigna estao  del lote desde select
            estado_str=request.form['estado']
            lote.estado=EstadoLote[estado_str]#convierte a string

        except Exception as e:
            # En caso de cualquier error durante la actualización, deshaz la transacción
            db.session.rollback()
            flash(f'Error al actualizar el lote: {e}', 'danger')
        db.session.commit()
        flash('Lote actualizado correctamente.', 'success')
        return redirect(url_for('loteVino_bp.listar_lotes'))

    return render_template('/lotes/editar_lotes.html', lote=lote, variedades=variedades , estados=EstadoLote, estado_actual=lote.estado), 200
