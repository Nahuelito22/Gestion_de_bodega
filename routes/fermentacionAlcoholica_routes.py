import uuid
from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash
from datetime import datetime
from models.fermentacionAlcoholica import FermentacionAlcoholica
from models.loteVino import LoteVino # Necesitamos importar LoteVino para el dropdown
from models.db import db

# Creamos el blueprint para fermentacionAlcoholica
fermentacion_bp = Blueprint('fermentacion_bp', __name__)

# =====================================================================
# RUTAS DE API (JSON) - Para Postman, otros servicios, etc.
# Estas rutas devuelven JSON.
# =====================================================================

# GET /api/fermentacion/ - Obtener todas las fermentaciones (API)
@fermentacion_bp.route('/', methods=['GET'])
def get_fermentaciones_api(): # Renombrado para diferenciar de la HTML
    fermentaciones = FermentacionAlcoholica.query.all()
    resultados = []
    for res in fermentaciones:
        lote_nombre = res.lote_vino.nombre_lote if res.lote_vino else "N/A"
        resultados.append({
            'id': res.id,
            'lote_vino_id': res.lote_vino_id,
            'lote_nombre': lote_nombre, # Añadido para la API
            'fecha_inicio': res.fecha_inicio.isoformat(),
            'fecha_fin': res.fecha_fin.isoformat() if res.fecha_fin else None, # Manejar si fecha_fin es None
            'temperatura_control_c': res.temperatura_control_c,
            'densidad_inicial': res.densidad_inicial,
            'densidad_final': res.densidad_final,
            'ph_medicion': res.ph_medicion,
            'acidez_volatil_g_l': res.acidez_volatil_g_l,
            'tipo_levadura': res.tipo_levadura,
            'notas': res.notas
        })
    return jsonify(resultados), 200

# GET /api/fermentacion/<id> - Obtener Fermentacion por ID (API)
@fermentacion_bp.route('/<string:id>', methods=['GET'])
def get_fermentacion_api(id): # Renombrado para diferenciar de la HTML
    res = FermentacionAlcoholica.query.get(id)
    if not res:
        return jsonify({'error': 'Fermentacion no encontrada'}), 404
    
    lote_nombre = res.lote_vino.nombre_lote if res.lote_vino else "N/A"
    return jsonify({
        'id': res.id,
        'lote_vino_id': res.lote_vino_id,
        'lote_nombre': lote_nombre, # Añadido para la API
        'fecha_inicio': res.fecha_inicio.isoformat(),
        'fecha_fin': res.fecha_fin.isoformat() if res.fecha_fin else None,
        'temperatura_control_c': res.temperatura_control_c,
        'densidad_inicial': res.densidad_inicial,
        'densidad_final': res.densidad_final,
        'ph_medicion': res.ph_medicion,
        'acidez_volatil_g_l': res.acidez_volatil_g_l,
        'tipo_levadura': res.tipo_levadura,
        'notas': res.notas
    }), 200

# POST /api/fermentacion/ - Crear nueva fermentación (API)
@fermentacion_bp.route('/', methods=['POST'])
def crear_fermentacion_api(): # Renombrado para diferenciar de la HTML
    data = request.get_json()

    # Validaciones para la API
    if not data or "lote_vino_id" not in data or "fecha_inicio" not in data:
        return jsonify({'Error': 'Faltan campos requeridos: lote_vino_id, fecha_inicio'}), 400
    
    # Validar si el lote_vino_id existe
    if not LoteVino.query.get(data['lote_vino_id']):
        return jsonify({'error': 'El lote de vino asociado no existe'}), 400

    try:
        fecha_inicio_dt = datetime.fromisoformat(data['fecha_inicio'])
        # fecha_fin es opcional en la API (si no se ha terminado la fermentación)
        fecha_fin_dt = datetime.fromisoformat(data['fecha_fin']) if 'fecha_fin' in data and data['fecha_fin'] else None
    except ValueError:
        return jsonify({'error': 'Formato de fecha inválido. Usar YYYY-MM-DD o YYYY-MM-DDTHH:MM:SS'}), 400
    
    nueva_fermentacion = FermentacionAlcoholica(
        lote_vino_id=data['lote_vino_id'],
        fecha_inicio=fecha_inicio_dt,
        fecha_fin=fecha_fin_dt,
        temperatura_control_c=data.get('temperatura_control_c'),
        densidad_inicial=data.get('densidad_inicial'),
        densidad_final=data.get('densidad_final'),
        ph_medicion=data.get('ph_medicion'),
        acidez_volatil_g_l=data.get('acidez_volatil_g_l'),
        tipo_levadura=data.get('tipo_levadura'),
        notas=data.get('notas')
    )

    db.session.add(nueva_fermentacion)
    db.session.commit()

    lote_nombre = nueva_fermentacion.lote_vino.nombre_lote if nueva_fermentacion.lote_vino else "N/A"
    return jsonify({
        'id': nueva_fermentacion.id,
        'lote_vino_id': nueva_fermentacion.lote_vino_id,
        'lote_nombre': lote_nombre,
        'fecha_inicio': nueva_fermentacion.fecha_inicio.isoformat(),
        'fecha_fin': nueva_fermentacion.fecha_fin.isoformat() if nueva_fermentacion.fecha_fin else None,
        'temperatura_control_c': nueva_fermentacion.temperatura_control_c,
        'densidad_inicial': nueva_fermentacion.densidad_inicial,
        'densidad_final': nueva_fermentacion.densidad_final,
        'ph_medicion': nueva_fermentacion.ph_medicion,
        'acidez_volatil_g_l': nueva_fermentacion.acidez_volatil_g_l,
        'tipo_levadura': nueva_fermentacion.tipo_levadura,
        'notas': nueva_fermentacion.notas
    }), 201

# PATCH /api/fermentacion/<id> - Modificar parcialmente fermentación (API)
@fermentacion_bp.route('/<string:id>', methods=['PATCH'])
def modificar_fermentacion_api(id): # Renombrado para diferenciar de la HTML
    fermentacion_cambio = FermentacionAlcoholica.query.get(id)
    if not fermentacion_cambio:
        return jsonify({'error': 'Fermentacion no encontrada'}), 404

    data = request.get_json()
    if not data:
        return jsonify({'error': 'No hay datos para actualizar'}), 400

    if 'lote_vino_id' in data:
        if not LoteVino.query.get(data['lote_vino_id']):
            return jsonify({'error': 'El nuevo lote de vino asociado no existe'}), 400
        fermentacion_cambio.lote_vino_id = data['lote_vino_id']

    try:
        if 'fecha_inicio' in data:
            fermentacion_cambio.fecha_inicio = datetime.fromisoformat(data['fecha_inicio'])
        if 'fecha_fin' in data:
            fermentacion_cambio.fecha_fin = datetime.fromisoformat(data['fecha_fin']) if data['fecha_fin'] else None
    except ValueError:
        return jsonify({'error': 'Formato de fecha inválido. Usar YYYY-MM-DD o YYYY-MM-DDTHH:MM:SS'}), 400

    if 'temperatura_control_c' in data:
        fermentacion_cambio.temperatura_control_c = data['temperatura_control_c']
    if 'densidad_inicial' in data:
        fermentacion_cambio.densidad_inicial = data['densidad_inicial']
    if 'densidad_final' in data:
        fermentacion_cambio.densidad_final = data['densidad_final']
    if 'ph_medicion' in data:
        fermentacion_cambio.ph_medicion = data['ph_medicion']
    if 'acidez_volatil_g_l' in data:
        fermentacion_cambio.acidez_volatil_g_l = data['acidez_volatil_g_l']
    if 'tipo_levadura' in data:
        fermentacion_cambio.tipo_levadura = data['tipo_levadura']
    if 'notas' in data:
        fermentacion_cambio.notas = data['notas']

    db.session.commit()

    lote_nombre = fermentacion_cambio.lote_vino.nombre_lote if fermentacion_cambio.lote_vino else "N/A"
    return jsonify({
        'id': fermentacion_cambio.id,
        'lote_vino_id': fermentacion_cambio.lote_vino_id,
        'lote_nombre': lote_nombre,
        'fecha_inicio': fermentacion_cambio.fecha_inicio.isoformat(),
        'fecha_fin': fermentacion_cambio.fecha_fin.isoformat() if fermentacion_cambio.fecha_fin else None,
        'temperatura_control_c': fermentacion_cambio.temperatura_control_c,
        'densidad_inicial': fermentacion_cambio.densidad_inicial,
        'densidad_final': fermentacion_cambio.densidad_final,
        'ph_medicion': fermentacion_cambio.ph_medicion,
        'acidez_volatil_g_l': fermentacion_cambio.acidez_volatil_g_l,
        'tipo_levadura': fermentacion_cambio.tipo_levadura,
        'notas': fermentacion_cambio.notas
    }), 200

# DELETE /api/fermentacion/<id> - Eliminar fermentación (API)
@fermentacion_bp.route('/<string:id>', methods=['DELETE'])
def borrar_fermentacion_api(id):
    fermentacion = FermentacionAlcoholica.query.get(id)
    if not fermentacion:
        return jsonify({'error': 'Fermentacion de uva no encontrada'}), 404
    
    db.session.delete(fermentacion)
    db.session.commit()
    return jsonify({'message': 'Fermentacion de uva eliminada exitosamente'}), 200

# =====================================================================
# RUTAS PARA LA INTERFAZ DE USUARIO (HTML) - Para el navegador web
# Estas rutas renderizan plantillas HTML o redirigen.
# =====================================================================

# Ruta para el menú principal de Fermentación
# URL: /fermentacion/menu
@fermentacion_bp.route('/menu', methods=['GET'])
def menu_fermentaciones():
    return render_template('fermentacion/menuFermentacion.html')

# Ruta para listar todas las fermentaciones (HTML)
# URL: /fermentacion/listar
@fermentacion_bp.route('/listar', methods=['GET'])
def listar_fermentaciones_html():
    fermentaciones = FermentacionAlcoholica.query.all()
    return render_template('fermentacion/listar_fermentaciones.html', fermentaciones=fermentaciones)

# Ruta para mostrar el formulario de creación de fermentación (GET HTML)
# URL: /fermentacion/crear
@fermentacion_bp.route('/crear', methods=['GET'])
def mostrar_formulario_fermentacion():
    lotes = LoteVino.query.all() # Necesitamos pasar los lotes para el dropdown
    return render_template('fermentacion/crear_fermentacion.html', lotes=lotes)

# Ruta para manejar el envío del formulario de creación de fermentación (POST HTML)
# URL: /fermentacion/crear
@fermentacion_bp.route('/crear', methods=['POST'])
def crear_fermentacion_html():
    lote_vino_id = request.form.get('lote_vino_id')
    fecha_inicio_str = request.form.get('fecha_inicio')
    fecha_fin_str = request.form.get('fecha_fin') # Opcional, puede estar vacío
    temperatura_control_c = request.form.get('temperatura_control_c')
    densidad_inicial = request.form.get('densidad_inicial')
    densidad_final = request.form.get('densidad_final')
    ph_medicion = request.form.get('ph_medicion')
    acidez_volatil_g_l = request.form.get('acidez_volatil_g_l')
    tipo_levadura = request.form.get('tipo_levadura')
    notas = request.form.get('notas')

    # Validar campos obligatorios
    if not lote_vino_id or not fecha_inicio_str:
        flash('Los campos Lote Asociado y Fecha de Inicio son obligatorios.', 'danger')
        return redirect(url_for('fermentacion_bp.mostrar_formulario_fermentacion'))

    # Convertir a los tipos de datos correctos y manejar errores
    try:
        fecha_inicio_dt = datetime.strptime(fecha_inicio_str, '%Y-%m-%d')
        # Fecha de fin es opcional, convertir solo si tiene valor
        fecha_fin_dt = datetime.strptime(fecha_fin_str, '%Y-%m-%d') if fecha_fin_str else None

        # Convertir a float solo si tienen valor, sino None
        temperatura_control_c_float = float(temperatura_control_c) if temperatura_control_c else None
        densidad_inicial_float = float(densidad_inicial) if densidad_inicial else None
        densidad_final_float = float(densidad_final) if densidad_final else None
        ph_medicion_float = float(ph_medicion) if ph_medicion else None
        acidez_volatil_g_l_float = float(acidez_volatil_g_l) if acidez_volatil_g_l else None

    except ValueError as e:
        flash(f'Error en el formato de datos: {e}. Asegúrate de ingresar números válidos y un formato de fecha correcto (AAAA-MM-DD).', 'danger')
        return redirect(url_for('fermentacion_bp.mostrar_formulario_fermentacion'))
    
    # Verificar si el lote_vino_id existe
    lote_existente = LoteVino.query.get(lote_vino_id)
    if not lote_existente:
        flash('El Lote de Vino seleccionado no existe. Por favor, crea el lote primero.', 'danger')
        return redirect(url_for('fermentacion_bp.mostrar_formulario_fermentacion'))

    # Crear la nueva instancia de FermentacionAlcoholica
    nueva_fermentacion = FermentacionAlcoholica(
        lote_vino_id=lote_vino_id,
        fecha_inicio=fecha_inicio_dt,
        fecha_fin=fecha_fin_dt,
        temperatura_control_c=temperatura_control_c_float,
        densidad_inicial=densidad_inicial_float,
        densidad_final=densidad_final_float,
        ph_medicion=ph_medicion_float,
        acidez_volatil_g_l=acidez_volatil_g_l_float,
        tipo_levadura=tipo_levadura,
        notas=notas
    )
    
    db.session.add(nueva_fermentacion)
    db.session.commit()
    flash('Registro de fermentación creado con éxito!', 'success')
    return redirect(url_for('fermentacion_bp.listar_fermentaciones_html'))

# Ruta para mostrar y procesar el formulario de edición de fermentación (GET/POST HTML)
# URL: /fermentacion/editar/<id>
@fermentacion_bp.route('/editar/<string:id>', methods=['GET', 'POST'])
def editar_fermentacion_html(id):
    fermentacion = FermentacionAlcoholica.query.get_or_404(id)
    lotes = LoteVino.query.all() # Necesitamos los lotes para el dropdown

    if request.method == 'POST':
        # Obtener datos del formulario (request.form)
        lote_vino_id = request.form.get('lote_vino_id')
        fecha_inicio_str = request.form.get('fecha_inicio')
        fecha_fin_str = request.form.get('fecha_fin')
        temperatura_control_c = request.form.get('temperatura_control_c')
        densidad_inicial = request.form.get('densidad_inicial')
        densidad_final = request.form.get('densidad_final')
        ph_medicion = request.form.get('ph_medicion')
        acidez_volatil_g_l = request.form.get('acidez_volatil_g_l')
        tipo_levadura = request.form.get('tipo_levadura')
        notas = request.form.get('notas')

        # Validar campos obligatorios
        if not lote_vino_id or not fecha_inicio_str:
            flash('Los campos Lote Asociado y Fecha de Inicio son obligatorios.', 'danger')
            return redirect(url_for('fermentacion_bp.editar_fermentacion_html', id=id))
        
        # Convertir a los tipos de datos correctos y manejar errores
        try:
            fermentacion.fecha_inicio = datetime.strptime(fecha_inicio_str, '%Y-%m-%d')
            fermentacion.fecha_fin = datetime.strptime(fecha_fin_str, '%Y-%m-%d') if fecha_fin_str else None

            fermentacion.temperatura_control_c = float(temperatura_control_c) if temperatura_control_c else None
            fermentacion.densidad_inicial = float(densidad_inicial) if densidad_inicial else None
            fermentacion.densidad_final = float(densidad_final) if densidad_final else None
            fermentacion.ph_medicion = float(ph_medicion) if ph_medicion else None
            fermentacion.acidez_volatil_g_l = float(acidez_volatil_g_l) if acidez_volatil_g_l else None

        except ValueError as e:
            flash(f'Error en el formato de datos: {e}. Asegúrate de ingresar números válidos y un formato de fecha correcto (AAAA-MM-DD).', 'danger')
            return redirect(url_for('fermentacion_bp.editar_fermentacion_html', id=id))
        
        # Verificar si el lote_vino_id existe
        lote_existente = LoteVino.query.get(lote_vino_id)
        if not lote_existente:
            flash('El Lote de Vino seleccionado no existe.', 'danger')
            return redirect(url_for('fermentacion_bp.editar_fermentacion_html', id=id))

        # Asignar los valores actualizados al objeto fermentacion
        fermentacion.lote_vino_id = lote_vino_id
        fermentacion.tipo_levadura = tipo_levadura
        fermentacion.notas = notas

        db.session.commit()
        flash('Registro de fermentación actualizado con éxito!', 'success')
        return redirect(url_for('fermentacion_bp.listar_fermentaciones_html'))

    # Si es un GET request, simplemente renderiza el formulario con los datos actuales
    return render_template('fermentacion/editar_fermentacion.html', fermentacion=fermentacion, lotes=lotes)

# Ruta para borrar una fermentación (POST HTML)
# URL: /fermentacion/borrar/<id>
@fermentacion_bp.route('/borrar/<string:id>', methods=['POST'])
def borrar_fermentacion_html(id):
    fermentacion = FermentacionAlcoholica.query.get_or_404(id)
    
    db.session.delete(fermentacion)
    db.session.commit()
    flash('Registro de fermentación eliminado exitosamente!', 'success')
    return redirect(url_for('fermentacion_bp.listar_fermentaciones_html'))