import uuid
import os
from werkzeug.utils import secure_filename
from flask import Blueprint, current_app, flash, redirect, render_template, request, jsonify, abort, url_for
from models.variedadUva import VariedadUva
from models.db import db

# Define la carpeta de subida de imágenes
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'static', 'images')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Creamos el blueprint para VariedadUva
variedadUva_bp = Blueprint('variedadUva_bp', __name__)

# --- Rutas API (JSON) ---

@variedadUva_bp.route('/api/', methods=['GET'])
def get_variedades_api():
    variedades = VariedadUva.query.all()
    resultado = []
    for v in variedades:
        foto_url = url_for('static', filename='images/' + v.foto_ruta) if v.foto_ruta else None
        resultado.append({
            "id": v.id,
            "nombre": v.nombre,
            "origen": v.origen,
            "foto_ruta": foto_url
        })
    return jsonify(resultado), 200

@variedadUva_bp.route('/api/<string:id>', methods=['GET'])
def get_variedad_api(id):
    variedad = VariedadUva.query.get(id)
    if not variedad:
        return jsonify({"error": "Variedad no encontrada"}), 404

    foto_url = url_for('static', filename='images/' + variedad.foto_ruta) if variedad.foto_ruta else None
    return jsonify({
        "id": variedad.id,
        "nombre": variedad.nombre,
        "origen": variedad.origen,
        "foto_ruta": foto_url
    }), 200

@variedadUva_bp.route('/api/<string:id>', methods=['PUT'])
def reemplazar_variedad_api(id):
    variedad = VariedadUva.query.get(id)
    if not variedad:
        return jsonify({"error": "Variedad no encontrada"}), 404

    data = request.get_json()
    if not data or "nombre" not in data:
        return jsonify({"error": "El campo 'nombre' es obligatorio"}), 400

    variedad.nombre = data["nombre"]
    variedad.origen = data.get("origen")
    variedad.foto_ruta = data.get("foto_ruta")

    db.session.commit()

    foto_url = url_for('static', filename='images/' + variedad.foto_ruta) if variedad.foto_ruta else None
    return jsonify({
        "id": variedad.id,
        "nombre": variedad.nombre,
        "origen": variedad.origen,
        "foto_ruta": foto_url
    }), 200

@variedadUva_bp.route('/api/<string:id>', methods=['PATCH'])
def modificar_variedad_api(id):
    variedad = VariedadUva.query.get(id)
    if not variedad:
        return jsonify({"error": "Variedad no encontrada"}), 404

    data = request.get_json()
    if not data:
        return jsonify({"error": "No hay datos para actualizar"}), 400

    if "nombre" in data:
        variedad.nombre = data["nombre"]
    if "origen" in data:
        variedad.origen = data["origen"]
    if "foto_ruta" in data:
        variedad.foto_ruta = data["foto_ruta"]

    db.session.commit()

    foto_url = url_for('static', filename='images/' + variedad.foto_ruta) if variedad.foto_ruta else None
    return jsonify({
        "id": variedad.id,
        "nombre": variedad.nombre,
        "origen": variedad.origen,
        "foto_ruta": foto_url
    }), 200

@variedadUva_bp.route('/api/<string:id>', methods=['DELETE'])
def eliminar_variedad_api(id):
    variedad = VariedadUva.query.get(id)
    if not variedad:
        return jsonify({"error": "Variedad no encontrada"}), 404

    if variedad.foto_ruta:
        image_path_on_disk = os.path.join(UPLOAD_FOLDER, variedad.foto_ruta)
        if os.path.exists(image_path_on_disk):
            os.remove(image_path_on_disk)

    db.session.delete(variedad)
    db.session.commit()

    return jsonify({"mensaje": f"Variedad {id} eliminada exitosamente"}), 200

# --- Rutas para la Interfaz de Usuario (HTML) ---

@variedadUva_bp.route('/listar', methods=['GET'])
def get_variedadesHtml():
    variedades = VariedadUva.query.all()
    return render_template('variedades/variedades.html', variedades=variedades), 200

@variedadUva_bp.route('/menu', methods=['GET'])
def menu_variedades():
    return render_template('variedades/menuVariedad.html')

@variedadUva_bp.route('/crear', methods=['GET'])
def mostrar_formulario_variedad():
    return render_template('variedades/crear.html')

@variedadUva_bp.route('/crear', methods=['POST'])
def crear_variedad():
    nombre = request.form.get('nombre')
    origen = request.form.get('origen')
    foto_ruta_file = request.files.get('foto_ruta')

    if not nombre:
        flash('El campo Nombre es obligatorio.', 'danger')
        return redirect(url_for('variedadUva_bp.mostrar_formulario_variedad'))

    ruta_guardado_bd = None

    if foto_ruta_file and foto_ruta_file.filename != '':
        if allowed_file(foto_ruta_file.filename):
            os.makedirs(UPLOAD_FOLDER, exist_ok=True)
            extension = os.path.splitext(foto_ruta_file.filename)[1]
            nombre_unico = str(uuid.uuid4()) + extension
            file_path = os.path.join(UPLOAD_FOLDER, nombre_unico)
            
            try:
                foto_ruta_file.save(file_path)
                ruta_guardado_bd = nombre_unico
            except Exception as e:
                flash(f'Error al guardar la imagen: {e}', 'danger')
                return redirect(url_for('variedadUva_bp.mostrar_formulario_variedad'))
        else:
            flash('Formato de imagen no permitido. Solo png, jpg, jpeg, gif.', 'danger')
            return redirect(url_for('variedadUva_bp.mostrar_formulario_variedad'))

    nueva_variedad = VariedadUva(
        nombre=nombre,
        origen=origen,
        foto_ruta=ruta_guardado_bd
    )

    db.session.add(nueva_variedad)
    db.session.commit()

    flash("Variedad creada con éxito!", "success")
    return redirect(url_for('variedadUva_bp.get_variedadesHtml'))

@variedadUva_bp.route('/editar/<string:id>', methods=['GET', 'POST'])
def editar_variedad(id):
    variedad = VariedadUva.query.get_or_404(id)

    if request.method == 'POST':
        variedad.nombre = request.form['nombre']
        variedad.origen = request.form['origen']

        foto_file = request.files.get('foto_ruta')

        if foto_file and foto_file.filename != '':
            if allowed_file(foto_file.filename):
                os.makedirs(UPLOAD_FOLDER, exist_ok=True)
                if variedad.foto_ruta:
                    old_path = os.path.join(UPLOAD_FOLDER, variedad.foto_ruta)
                    if os.path.exists(old_path):
                        os.remove(old_path)
                
                extension = os.path.splitext(foto_file.filename)[1]
                nombre_unico = str(uuid.uuid4()) + extension
                new_file_path = os.path.join(UPLOAD_FOLDER, nombre_unico)
                foto_file.save(new_file_path)
                
                variedad.foto_ruta = nombre_unico
            else:
                flash('Formato de imagen no permitido.', 'danger')
                return redirect(url_for('variedadUva_bp.editar_variedad', id=id))

        db.session.commit()
        flash('Variedad actualizada correctamente.', 'success')
        return redirect(url_for('variedadUva_bp.get_variedadesHtml'))

    return render_template('variedades/editar.html', variedad=variedad)

@variedadUva_bp.route('/delete/<string:id>', methods=['POST'])
def borrar_variedad(id):
    variedad = VariedadUva.query.get_or_404(id)

    db.session.refresh(variedad)

    if variedad.foto_ruta:
        image_path_on_disk = os.path.join(UPLOAD_FOLDER, variedad.foto_ruta)
        if os.path.exists(image_path_on_disk):
            os.remove(image_path_on_disk)

    db.session.delete(variedad)
    db.session.commit()
    flash('Variedad eliminada exitosamente!', 'success')
    return redirect(url_for('variedadUva_bp.get_variedadesHtml'))

# NUEVA RUTA: Para ver detalles de una variedad en HTML
@variedadUva_bp.route('/<string:id>/detalle', methods=['GET'])
def detalle_variedad(id):
    variedad = VariedadUva.query.get_or_404(id)
    return render_template('variedades/detalle.html', variedad=variedad), 200