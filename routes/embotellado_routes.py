import uuid
from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash
from datetime import datetime
from models.embotellado import Embotellado
from models.loteVino import LoteVino # Necesitamos importar LoteVino para el dropdown
from models.db import db
from flask_login import login_required

from models.estados.estado_embotellamiento import EstadoEmbotellado
# Creamos el blueprint para embotellado
embotellado_bp = Blueprint('embotellado_bp', __name__)

# RUTAS DE API (JSON) - Para Postman
# GET /api/embotellado/ - Obtener todos los embotellados (API)
@embotellado_bp.route('/api/', methods=['GET']) # CAMBIO IMPORTANTE AQUÍ
def get_embotellamientos_api(): # Renombrado para diferenciar de la HTML
    embotellamientos = Embotellado.query.all()
    resultados = []
    for res in embotellamientos:
        # CORREGIDO: Usar 'nombre_identificativo' en lugar de 'nombre_lote'
        lote_nombre = res.lote_vino.nombre_identificativo if res.lote_vino else "N/A"
        resultados.append({
            'id': res.id,
            'lote_vino_id': res.lote_vino_id,
            'lote_nombre': lote_nombre, # Añadido para la API
            'fecha_embotellado': res.fecha_embotellado.isoformat(),
            'numero_botellas_producidas': res.numero_botellas_producidas,
            'volumen_por_botella_ml': res.volumen_por_botella_ml,
            'ph_final': res.ph_final,
            'acidez_final_g_l': res.acidez_final_g_l,
            'grado_alcoholico_final_porcentaje': res.grado_alcoholico_final_porcentaje,
            'notas': res.notas
        })
    return jsonify(resultados), 200

# GET /api/embotellado/<id> - Obtener Embotellado por ID (API)
@embotellado_bp.route('/api/<string:id>', methods=['GET']) # CAMBIO IMPORTANTE AQUÍ
def get_embotellamiento_api(id): # Renombrado para diferenciar de la HTML
    res = Embotellado.query.get(id)
    if not res:
        return jsonify({'error': 'Embotellamiento no encontrado'}), 404 # Añadido 404
    
    # CORREGIDO: Usar 'nombre_identificativo' en lugar de 'nombre_lote'
    lote_nombre = res.lote_vino.nombre_identificativo if res.lote_vino else "N/A"
    return jsonify({
        'id': res.id,
        'lote_vino_id': res.lote_vino_id,
        'lote_nombre': lote_nombre, # Añadido para la API
        'fecha_embotellado': res.fecha_embotellado.isoformat(),
        'numero_botellas_producidas': res.numero_botellas_producidas,
        'volumen_por_botella_ml': res.volumen_por_botella_ml,
        'ph_final': res.ph_final,
        'acidez_final_g_l': res.acidez_final_g_l,
        'grado_alcoholico_final_porcentaje': res.grado_alcoholico_final_porcentaje,
        'notas': res.notas
    }), 200

# POST /api/embotellado/ - Crear nuevo embotellado (API)
@embotellado_bp.route('/api/', methods=['POST']) # CAMBIO IMPORTANTE AQUÍ
def crear_embotellamiento_api(): # Renombrado para diferenciar de la HTML
    data = request.get_json()

    # Validaciones para la API
    if not data or 'lote_vino_id' not in data or 'fecha_embotellado' not in data:
        return jsonify({'Error': 'Faltan campos requeridos: lote_vino_id, fecha_embotellado'}), 400
    
    # Validar si el lote_vino_id existe
    if not LoteVino.query.get(data['lote_vino_id']):
        return jsonify({'error': 'El lote de vino asociado no existe'}), 400

    try:
        fecha_embotellado_dt = datetime.fromisoformat(data['fecha_embotellado'])
    except ValueError:
        return jsonify({'error': 'Formato de fecha inválido. Usar YYYY-MM-DD o YYYY-MM-DDTHH:MM:SS'}), 400
    
    nuevo_embotellado = Embotellado(
        lote_vino_id=data['lote_vino_id'],
        fecha_embotellado=fecha_embotellado_dt,
        numero_botellas_producidas=data.get('numero_botellas_producidas'), # Usar .get() para nullable
        volumen_por_botella_ml=data.get('volumen_por_botella_ml'),
        ph_final=data.get('ph_final'),
        acidez_final_g_l=data.get('acidez_final_g_l'),
        grado_alcoholico_final_porcentaje=data.get('grado_alcoholico_final_porcentaje'),
        notas=data.get('notas')
    )

    db.session.add(nuevo_embotellado)
    db.session.commit()

    # CORREGIDO: Usar 'nombre_identificativo' en lugar de 'nombre_lote'
    lote_nombre = nuevo_embotellado.lote_vino.nombre_identificativo if nuevo_embotellado.lote_vino else "N/A"
    return jsonify({
        'id': nuevo_embotellado.id,
        'lote_vino_id': nuevo_embotellado.lote_vino_id,
        'lote_nombre': lote_nombre,
        'fecha_embotellado': nuevo_embotellado.fecha_embotellado.isoformat(),
        'numero_botellas_producidas': nuevo_embotellado.numero_botellas_producidas,
        'volumen_por_botella_ml': nuevo_embotellado.volumen_por_botella_ml,
        'ph_final': nuevo_embotellado.ph_final,
        'acidez_final_g_l': nuevo_embotellado.acidez_final_g_l,
        'grado_alcoholico_final_porcentaje': nuevo_embotellado.grado_alcoholico_final_porcentaje,
        'notas': nuevo_embotellado.notas
    }), 201

# PATCH /api/embotellado/<id> - Modificar parcialmente embotellado (API)
@embotellado_bp.route('/api/<string:id>', methods=['PATCH']) # CAMBIO IMPORTANTE AQUÍ
def modificar_embotellado_api(id): # Renombrado para diferenciar de la HTML
    cambio_embotellado = Embotellado.query.get(id)
    if not cambio_embotellado:
        return jsonify({'error': 'Embotellado no encontrado'}), 404
    
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No hay datos para actualizar'}), 400 # Cambiado el mensaje

    if 'lote_vino_id' in data:
        if not LoteVino.query.get(data['lote_vino_id']):
            return jsonify({'error': 'El nuevo lote de vino asociado no existe'}), 400
        cambio_embotellado.lote_vino_id = data['lote_vino_id']

    try:
        if 'fecha_embotellado' in data:
            cambio_embotellado.fecha_embotellado = datetime.fromisoformat(data['fecha_embotellado'])
    except ValueError:
        return jsonify({'error': 'Formato de fecha inválido. Usar YYYY-MM-DD o YYYY-MM-DDTHH:MM:SS'}), 400
    
    if 'numero_botellas_producidas' in data:
        cambio_embotellado.numero_botellas_producidas = data['numero_botellas_producidas']
    if 'volumen_por_botella_ml' in data:
        cambio_embotellado.volumen_por_botella_ml = data['volumen_por_botella_ml']
    if 'ph_final' in data:
        cambio_embotellado.ph_final = data['ph_final']
    if 'acidez_final_g_l' in data:
        cambio_embotellado.acidez_final_g_l = data['acidez_final_g_l']
    if 'grado_alcoholico_final_porcentaje' in data:
        cambio_embotellado.grado_alcoholico_final_porcentaje = data['grado_alcoholico_final_porcentaje']
    if 'notas' in data:
        cambio_embotellado.notas = data['notas']

    db.session.commit()
    # CORREGIDO: Usar 'nombre_identificativo' en lugar de 'nombre_lote'
    lote_nombre = cambio_embotellado.lote_vino.nombre_identificativo if cambio_embotellado.lote_vino else "N/A"
    return jsonify({
        'id': cambio_embotellado.id,
        'lote_vino_id': cambio_embotellado.lote_vino_id,
        'lote_nombre': lote_nombre,
        'fecha_embotellado': cambio_embotellado.fecha_embotellado.isoformat(),
        'numero_botellas_producidas': cambio_embotellado.numero_botellas_producidas,
        'volumen_por_botella_ml': cambio_embotellado.volumen_por_botella_ml,
        'ph_final': cambio_embotellado.ph_final,
        'acidez_final_g_l': cambio_embotellado.acidez_final_g_l,
        'grado_alcoholico_final_porcentaje': cambio_embotellado.grado_alcoholico_final_porcentaje,
        'notas': cambio_embotellado.notas
    }), 200

# DELETE /api/embotellado/<id> - Eliminar embotellado (API)
@embotellado_bp.route('/api/<string:id>', methods=['DELETE']) # CAMBIO IMPORTANTE AQUÍ
def borrar_embotellado_api(id):
    embotellado = Embotellado.query.get(id)
    if not embotellado:
        return jsonify({'error': 'Embotellado no encontrado'}), 404
    
    db.session.delete(embotellado)
    db.session.commit()
    return jsonify({'message': 'Embotellado eliminado exitosamente'}), 200


# RUTAS PARA LA INTERFAZ DE USUARIO (HTML)
# URL: /embotellado/menu
@embotellado_bp.route('/menu', methods=['GET'])
@login_required
def menu_embotellados():
    return render_template('embotellado/menuEmbotellado.html')

# Ruta para listar todos los embotellados (HTML)
# URL: /embotellado/listar
@embotellado_bp.route('/listar', methods=['GET'])
@login_required
def listar_embotellados_html():
    embotellados = Embotellado.query.all()
    estados=list(EstadoEmbotellado)

    return render_template('embotellado/listar_embotellados.html', embotellados=embotellados, estados=estados)

# Ruta para mostrar el formulario de creación de embotellado (GET HTML)
# URL: /embotellado/crear
@embotellado_bp.route('/crear', methods=['GET'])
@login_required
def mostrar_formulario_embotellado():
    lotes = LoteVino.query.all() # Necesitamos pasar los lotes para el dropdown
    estados=list(EstadoEmbotellado)
    return render_template('embotellado/crear_embotellado.html', lotes=lotes, estados=estados)

# Ruta para manejar el envío del formulario de creación de embotellado (POST HTML)
# URL: /embotellado/crear
@embotellado_bp.route('/crear', methods=['POST'])
@login_required
def crear_embotellado_html():
    estado=request.form['estado']
    estado_enum=EstadoEmbotellado[estado]

    lote_vino_id = request.form.get('lote_vino_id')
    fecha_embotellado_str = request.form.get('fecha_embotellado')
    numero_botellas_producidas = request.form.get('numero_botellas_producidas')
    volumen_por_botella_ml = request.form.get('volumen_por_botella_ml')
    ph_final = request.form.get('ph_final')
    acidez_final_g_l = request.form.get('acidez_final_g_l')
    grado_alcoholico_final_porcentaje = request.form.get('grado_alcoholico_final_porcentaje')
    notas = request.form.get('notas')

    # Validar campos obligatorios (lote y fecha de embotellado)
    if not lote_vino_id or not fecha_embotellado_str:
        flash('Los campos Lote Asociado y Fecha de Embotellado son obligatorios.', 'danger')
        return redirect(url_for('embotellado_bp.mostrar_formulario_embotellado'))

    # Convertir a los tipos de datos correctos y manejar errores
    try:
        fecha_embotellado_dt = datetime.strptime(fecha_embotellado_str, '%Y-%m-%d')
        
        # Convertir a int/float solo si tienen valor, sino None
        numero_botellas_producidas_int = int(numero_botellas_producidas) if numero_botellas_producidas else None
        volumen_por_botella_ml_float = float(volumen_por_botella_ml) if volumen_por_botella_ml else None
        ph_final_float = float(ph_final) if ph_final else None
        acidez_final_g_l_float = float(acidez_final_g_l) if acidez_final_g_l else None
        grado_alcoholico_final_porcentaje_float = float(grado_alcoholico_final_porcentaje) if grado_alcoholico_final_porcentaje else None

    except ValueError as e:
        flash(f'Error en el formato de datos: {e}. Asegúrate de ingresar números válidos y un formato de fecha correcto (AAAA-MM-DD).', 'danger')
        return redirect(url_for('embotellado_bp.mostrar_formulario_embotellado'))
    
    # Verificar si el lote_vino_id existe
    lote_existente = LoteVino.query.get(lote_vino_id)
    if not lote_existente:
        flash('El Lote de Vino seleccionado no existe. Por favor, crea el lote primero.', 'danger')
        return redirect(url_for('embotellado_bp.mostrar_formulario_embotellado'))

    # Crear la nueva instancia de Embotellado
    nuevo_embotellado = Embotellado(
        lote_vino_id=lote_vino_id,
        fecha_embotellado=fecha_embotellado_dt,
        numero_botellas_producidas=numero_botellas_producidas_int,
        volumen_por_botella_ml=volumen_por_botella_ml_float,
        ph_final=ph_final_float,
        acidez_final_g_l=acidez_final_g_l_float,
        grado_alcoholico_final_porcentaje=grado_alcoholico_final_porcentaje_float,
        notas=notas,
        estado=estado_enum
    )
    
    db.session.add(nuevo_embotellado)
    db.session.commit()
    flash('Registro de embotellado creado con éxito!', 'success')
    return redirect(url_for('embotellado_bp.listar_embotellados_html'))

# Ruta para mostrar y procesar el formulario de edición de embotellado (GET/POST HTML)
# URL: /embotellado/editar/<id>
@embotellado_bp.route('/editar/<string:id>', methods=['GET', 'POST'])
@login_required
def editar_embotellado_html(id):
    embotellado = Embotellado.query.get_or_404(id)
    lotes = LoteVino.query.all() # Necesitamos los lotes para el dropdown

    if request.method == 'POST':
        estado_str=request.form['estado']
        embotellado.estado=EstadoEmbotellado(estado_str)
        # Obtener datos del formulario (request.form)
        lote_vino_id = request.form.get('lote_vino_id')
        fecha_embotellado_str = request.form.get('fecha_embotellado')
        numero_botellas_producidas = request.form.get('numero_botellas_producidas')
        volumen_por_botella_ml = request.form.get('volumen_por_botella_ml')
        ph_final = request.form.get('ph_final')
        acidez_final_g_l = request.form.get('acidez_final_g_l')
        grado_alcoholico_final_porcentaje = request.form.get('grado_alcoholico_final_porcentaje')
        notas = request.form.get('notas')

        # Validar campos obligatorios
        if not lote_vino_id or not fecha_embotellado_str:
            flash('Los campos Lote Asociado y Fecha de Embotellado son obligatorios.', 'danger')
            return redirect(url_for('embotellado_bp.editar_embotellado_html', id=id))
        
        # Convertir a los tipos de datos correctos y manejar errores
        try:
            embotellado.fecha_embotellado = datetime.strptime(fecha_embotellado_str, '%Y-%m-%d')

            embotellado.numero_botellas_producidas = int(numero_botellas_producidas) if numero_botellas_producidas else None
            embotellado.volumen_por_botella_ml = float(volumen_por_botella_ml) if volumen_por_botella_ml else None
            embotellado.ph_final = float(ph_final) if ph_final else None
            embotellado.acidez_final_g_l = float(acidez_final_g_l) if acidez_final_g_l else None
            embotellado.grado_alcoholico_final_porcentaje = float(grado_alcoholico_final_porcentaje) if grado_alcoholico_final_porcentaje else None

        except ValueError as e:
            flash(f'Error en el formato de datos: {e}. Asegúrate de ingresar números válidos y un formato de fecha correcto (AAAA-MM-DD).', 'danger')
            return redirect(url_for('embotellado_bp.editar_embotellado_html', id=id))
        
        # Verificar si el lote_vino_id existe
        lote_existente = LoteVino.query.get(lote_vino_id)
        if not lote_existente:
            flash('El Lote de Vino seleccionado no existe.', 'danger')
            return redirect(url_for('embotellado_bp.editar_embotellado_html', id=id))

        # Asignar los valores actualizados al objeto embotellado
        embotellado.lote_vino_id = lote_vino_id
        embotellado.notas = notas

        db.session.commit()
        flash('Registro de embotellado actualizado con éxito!', 'success')
        return redirect(url_for('embotellado_bp.listar_embotellados_html'))

    # Si es un GET request, simplemente renderiza el formulario con los datos actuales
    return render_template('embotellado/editar_embotellado.html', embotellado=embotellado, lotes=lotes , estado_actual=embotellado.estado, estados=EstadoEmbotellado),200

# Ruta para borrar un embotellado (POST HTML)
# URL: /embotellado/borrar/<id>
@embotellado_bp.route('/borrar/<string:id>', methods=['POST'])
@login_required
def borrar_embotellado_html(id):
    embotellado = Embotellado.query.get_or_404(id)
    
    db.session.delete(embotellado)
    db.session.commit()
    flash('Registro de embotellado eliminado exitosamente!', 'success')
    return redirect(url_for('embotellado_bp.listar_embotellados_html'))


# Ruta principal para el blueprint (redirecciona al menú HTML)
@embotellado_bp.route('/', methods=['GET'])
@login_required
def index_embotellado():
    return redirect(url_for('embotellado_bp.menu_embotellados'))