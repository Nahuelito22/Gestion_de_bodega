import uuid
from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash
from datetime import datetime
from models.RecepcionUva import RecepcionUva
from models.loteVino import LoteVino # Necesitas importar LoteVino para usarlo en los formularios HTML
from models.db import db # Asumiendo que tu objeto db está en models/db.py

# Creamos el blueprint para recepcionUva
recepcionUva_bp = Blueprint('recepcionUva_bp', __name__)

# RUTAS DE API (JSON) - Para Postman
# GET /api/recepcion/ - Obtener todas las recepciones de uva (API)
@recepcionUva_bp.route('/', methods=['GET'])
def get_recepcionesUva_api(): # Renombrado para diferenciar de la HTML
    recepciones = RecepcionUva.query.all()
    resultados = []
    for r in recepciones:
        # Aquí puedes incluir los datos del lote asociado si lo necesitas en tu API
        lote_nombre = r.lote_vino.nombre_lote if r.lote_vino else "N/A"
        resultados.append({
            'id': r.id,
            'lote_vino_id': r.lote_vino_id,
            'lote_nombre': lote_nombre, # Añadido el nombre del lote para mayor claridad en la API
            'fecha_recepcion': r.fecha_recepcion.isoformat(),
            'cantidad_kg': r.cantidad_kg,
            'ph': r.ph,
            'acidez_total_g_l': r.acidez_total_g_l,
            'azucar_brix': r.azucar_brix,
            'notas': r.notas
        })
    return jsonify(resultados), 200

# GET /api/recepcion/<id> - Obtener Recepcion por ID (API)
@recepcionUva_bp.route('/<string:id>', methods=['GET'])
def get_recepcion_api(id): # Renombrado para diferenciar de la HTML
    recepcion = RecepcionUva.query.get(id)
    if not recepcion:
        return jsonify({'error': 'Recepción no encontrada'}), 404
    
    lote_nombre = recepcion.lote_vino.nombre_lote if recepcion.lote_vino else "N/A"
    return jsonify({
        'id': recepcion.id,
        'lote_vino_id': recepcion.lote_vino_id,
        'lote_nombre': lote_nombre, # Añadido el nombre del lote
        'fecha_recepcion': recepcion.fecha_recepcion.isoformat(),
        'cantidad_kg': recepcion.cantidad_kg,
        'ph': recepcion.ph,
        'acidez_total_g_l': recepcion.acidez_total_g_l,
        'azucar_brix': recepcion.azucar_brix,
        'notas': recepcion.notas
    }), 200

# POST /api/recepcion/ - Crear nueva recepción (API)
@recepcionUva_bp.route('/', methods=['POST'])
def crea_recepcion_api(): # Renombrado para diferenciar de la HTML
    data = request.get_json()

    # Validar campos obligatorios
    if not data or 'lote_vino_id' not in data or 'cantidad_kg' not in data or 'fecha_recepcion' not in data:
        return jsonify({'error': 'Faltan campos requeridos: lote_vino_id, cantidad_kg, fecha_recepcion'}), 400
    
    # Validar si el lote_vino_id existe
    if not LoteVino.query.get(data['lote_vino_id']):
        return jsonify({'error': 'El lote de vino asociado no existe'}), 400

    try:
        fecha_recepcion = datetime.fromisoformat(data['fecha_recepcion'])
    except ValueError:
        return jsonify({'error': 'Formato de fecha inválido. Usar YYYY-MM-DD o YYYY-MM-DDTHH:MM:SS'}), 400
    
    # Crear la nueva recepción con datos de la petición JSON
    nueva_recepcion = RecepcionUva(
        lote_vino_id=data['lote_vino_id'],
        fecha_recepcion=fecha_recepcion,
        cantidad_kg=data['cantidad_kg'],
        ph=data.get('ph'), # Usar .get() para campos opcionales, devuelve None si no están
        acidez_total_g_l=data.get('acidez_total_g_l'),
        azucar_brix=data.get('azucar_brix'),
        notas=data.get('notas'),
    )
    
    db.session.add(nueva_recepcion)
    db.session.commit()

    # Devolver la nueva recepción creada
    lote_nombre = nueva_recepcion.lote_vino.nombre_lote if nueva_recepcion.lote_vino else "N/A"
    return jsonify({
        'id': nueva_recepcion.id,
        'lote_vino_id': nueva_recepcion.lote_vino_id,
        'lote_nombre': lote_nombre,
        'fecha_recepcion': nueva_recepcion.fecha_recepcion.isoformat(),
        'cantidad_kg': nueva_recepcion.cantidad_kg,
        'ph': nueva_recepcion.ph,
        'acidez_total_g_l': nueva_recepcion.acidez_total_g_l,
        'azucar_brix': nueva_recepcion.azucar_brix,
        'notas': nueva_recepcion.notas
    }), 201

# PATCH /api/recepcion/<id> - Modificar parcialmente recepción (API)
@recepcionUva_bp.route('/<string:id>', methods=['PATCH'])
def modificar_recepcion_api(id): # Renombrado para diferenciar de la HTML
    recepcion_cambio = RecepcionUva.query.get(id)
    if not recepcion_cambio:
        return jsonify({'error': 'Recepción de uva no encontrada'}), 404
    
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No hay datos para actualizar'}), 400

    if 'lote_vino_id' in data:
        # Opcional: Validar si el nuevo lote_vino_id existe
        if not LoteVino.query.get(data['lote_vino_id']):
            return jsonify({'error': 'El nuevo lote de vino asociado no existe'}), 400
        recepcion_cambio.lote_vino_id = data['lote_vino_id']
    
    if 'fecha_recepcion' in data:
        try:
            recepcion_cambio.fecha_recepcion = datetime.fromisoformat(data['fecha_recepcion'])
        except ValueError:
            return jsonify({'error': 'Formato de fecha inválido. Usar YYYY-MM-DD o YYYY-MM-DDTHH:MM:SS'}), 400
    
    if 'cantidad_kg' in data:
        recepcion_cambio.cantidad_kg = data['cantidad_kg']
    if 'ph' in data:
        recepcion_cambio.ph = data['ph']
    if 'acidez_total_g_l' in data:
        recepcion_cambio.acidez_total_g_l = data['acidez_total_g_l']
    if 'azucar_brix' in data:
        recepcion_cambio.azucar_brix = data['azucar_brix']
    if 'notas' in data:
        recepcion_cambio.notas = data['notas']
    
    db.session.commit()

    lote_nombre = recepcion_cambio.lote_vino.nombre_lote if recepcion_cambio.lote_vino else "N/A"
    return jsonify({
        'id': recepcion_cambio.id,
        'lote_vino_id': recepcion_cambio.lote_vino_id,
        'lote_nombre': lote_nombre,
        'fecha_recepcion': recepcion_cambio.fecha_recepcion.isoformat(),
        'cantidad_kg': recepcion_cambio.cantidad_kg,
        'ph': recepcion_cambio.ph,
        'acidez_total_g_l': recepcion_cambio.acidez_total_g_l,
        'azucar_brix': recepcion_cambio.azucar_brix,
        'notas': recepcion_cambio.notas
    }), 200

# DELETE /api/recepcion/<id> - Eliminar recepción (API)
@recepcionUva_bp.route('/<string:id>', methods=['DELETE'])
def borrar_recepcion_api(id):
    recepcion = RecepcionUva.query.get(id)
    if not recepcion:
        return jsonify({'error': 'Recepción de uva no encontrada'}), 404
    
    db.session.delete(recepcion)
    db.session.commit()
    return jsonify({'message': 'Recepción de uva eliminada exitosamente'}), 200

# RUTAS PARA LA INTERFAZ DE USUARIO (HTML) 
# Ruta para el menú principal de Recepción
# URL: /recepcion/menu
@recepcionUva_bp.route('/menu', methods=['GET'])
def menu_recepciones():
    return render_template('recepcion/menuRecepcion.html')

# Ruta para listar todas las recepciones de uva (HTML)
# URL: /recepcion/listar
@recepcionUva_bp.route('/listar', methods=['GET'])
def listar_recepciones_html():
    recepciones = RecepcionUva.query.all()
    # Las relaciones en SQLAlchemy permiten acceder al lote_vino directamente
    return render_template('recepcion/listar_recepciones.html', recepciones=recepciones)

# Ruta para mostrar el formulario de creación de recepción (GET HTML)
# URL: /recepcion/crear
@recepcionUva_bp.route('/crear', methods=['GET'])
def mostrar_formulario_recepcion():
    lotes_disponibles  = LoteVino.query.all() # Necesitamos pasar todos los lotes existentes para el dropdown
    return render_template('recepcion/crear_recepcion.html', lotes_disponibles=lotes_disponibles)

# Ruta para manejar el envío del formulario de creación de recepción (POST HTML)
# URL: /recepcion/crear
@recepcionUva_bp.route('/crear', methods=['POST'])
def crear_recepcion_html():
    
    lotes=LoteVino.query.all()
    # Obtener datos del formulario (request.form)
    lote_vino_id = request.form.get('lote_vino_id')
    fecha_recepcion_str = request.form.get('fecha_recepcion')
    cantidad_kg = request.form.get('cantidad_kg')
    ph = request.form.get('ph')
    acidez_total_g_l = request.form.get('acidez_total_g_l')
    azucar_brix = request.form.get('azucar_brix')
    notas = request.form.get('notas')

    # Validar campos obligatorios
    if not lote_vino_id or not fecha_recepcion_str or not cantidad_kg:
        flash('Los campos Lote, Fecha y Cantidad son obligatorios.', 'danger')
        return redirect(url_for('recepcionUva_bp.mostrar_formulario_recepcion'))

    # Convertir a los tipos de datos correctos y manejar errores de conversión
    try:
        fecha_recepcion = datetime.strptime(fecha_recepcion_str, '%Y-%m-%d') # Formato de fecha del input type="date"
        cantidad_kg = float(cantidad_kg)
        # Convertir campos opcionales solo si tienen valor, sino dejarlos como None
        ph = float(ph) if ph else None 
        acidez_total_g_l = float(acidez_total_g_l) if acidez_total_g_l else None
        azucar_brix = float(azucar_brix) if azucar_brix else None
    except ValueError as e:
        flash(f'Error en el formato de datos: {e}. Asegúrate de ingresar números válidos y un formato de fecha correcto (AAAA-MM-DD).', 'danger')
        return redirect(url_for('recepcionUva_bp.mostrar_formulario_recepcion'))
    
    # Verificar si el lote_vino_id existe en la base de datos
    lote_existente = LoteVino.query.get(lote_vino_id)
    if not lote_existente:
        flash('El Lote de Vino seleccionado no existe. Por favor, crea el lote primero.', 'danger')
        return redirect(url_for('recepcionUva_bp.mostrar_formulario_recepcion'))

    # Crear la nueva instancia de RecepcionUva
    nueva_recepcion = RecepcionUva(
        lote_vino_id=lote_vino_id,
        fecha_recepcion=fecha_recepcion,
        cantidad_kg=cantidad_kg,
        ph=ph,
        acidez_total_g_l=acidez_total_g_l,
        azucar_brix=azucar_brix,
        notas=notas
    )
    
    db.session.add(nueva_recepcion)
    db.session.commit()
    flash('Recepción de uva creada con éxito!', 'success')
    return redirect(url_for('recepcionUva_bp.listar_recepciones_html'))

# Ruta para mostrar y procesar el formulario de edición de recepción (GET/POST HTML)
# URL: /recepcion/editar/<id>
@recepcionUva_bp.route('/editar/<string:id>', methods=['GET', 'POST'])
def editar_recepcion_html(id):
    recepcion = RecepcionUva.query.get_or_404(id) # Obtiene la recepción o devuelve 404
    lotes_disponibles = LoteVino.query.all() # Necesitamos los lotes para el dropdown en el formulario

    if request.method == 'POST':
        # Obtener datos del formulario (request.form)
        lote_vino_id = request.form.get('lote_vino_id')
        fecha_recepcion_str = request.form.get('fecha_recepcion')
        cantidad_kg = request.form.get('cantidad_kg')
        ph = request.form.get('ph')
        acidez_total_g_l = request.form.get('acidez_total_g_l')
        azucar_brix = request.form.get('azucar_brix')
        notas = request.form.get('notas')

        # Validar campos obligatorios
        if not lote_vino_id or not fecha_recepcion_str or not cantidad_kg:
            flash('Los campos Lote, Fecha y Cantidad son obligatorios.', 'danger')
            return redirect(url_for('recepcionUva_bp.editar_recepcion_html', id=id))
        
        # Convertir a los tipos de datos correctos y manejar errores de conversión
        try:
            recepcion.fecha_recepcion = datetime.strptime(fecha_recepcion_str, '%Y-%m-%d')
            recepcion.cantidad_kg = float(cantidad_kg)
            recepcion.ph = float(ph) if ph else None
            recepcion.acidez_total_g_l = float(acidez_total_g_l) if acidez_total_g_l else None
            recepcion.azucar_brix = float(azucar_brix) if azucar_brix else None
        except ValueError as e:
            flash(f'Error en el formato de datos: {e}. Asegúrate de ingresar números válidos y un formato de fecha correcto (AAAA-MM-DD).', 'danger')
            return redirect(url_for('recepcionUva_bp.editar_recepcion_html', id=id))
        
        # Verificar si el lote_vino_id existe
        lote_existente = LoteVino.query.get(lote_vino_id)
        if not lote_existente:
            flash('El Lote de Vino seleccionado no existe.', 'danger')
            return redirect(url_for('recepcionUva_bp.editar_recepcion_html', id=id))
        
        # Asignar los valores actualizados al objeto recepcion
        recepcion.lote_vino_id = lote_vino_id
        recepcion.notas = notas

        db.session.commit()
        flash('Recepción de uva actualizada con éxito!', 'success')
        return redirect(url_for('recepcionUva_bp.listar_recepciones_html'))

    # Si es un GET request, simplemente renderiza el formulario con los datos actuales
    return render_template('recepcion/editar_recepcion.html', recepcion=recepcion, lotes_disponibles=lotes_disponibles)

# Ruta para borrar una recepción de uva (POST HTML)
# URL: /recepcion/borrar/<id>
@recepcionUva_bp.route('/borrar/<string:id>', methods=['POST'])
def borrar_recepcion_html(id):
    recepcion = RecepcionUva.query.get_or_404(id) # Obtiene la recepción o devuelve 404
    
    db.session.delete(recepcion)
    db.session.commit()
    flash('Recepción de uva eliminada exitosamente!', 'success')
    return redirect(url_for('recepcionUva_bp.listar_recepciones_html'))
