import uuid
import os
from werkzeug.utils import secure_filename
from flask import Blueprint, current_app, flash, redirect, render_template, request, jsonify, abort, url_for
from models.variedadUva import VariedadUva
from models.db import db



UPLOAD_FOLDER = 'static/images'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Creamos el blueprint para VariedadUva
variedadUva_bp = Blueprint('variedadUva_bp', __name__)

# GET / Obtener todas las variedades
@variedadUva_bp.route('/', methods=['GET'])
def get_variedades():
    variedades = VariedadUva.query.all()  # Traemos todas
    resultado = []
    for v in variedades:
        resultado.append({
            "id": v.id,
            "nombre": v.nombre,
            "origen": v.origen,
            "foto_ruta": v.foto_ruta
        })
    return jsonify(resultado), 200


# GET / Obtener variedad por ID
@variedadUva_bp.route('/<string:id>', methods=['GET'])
def get_variedad(id):
    variedad = VariedadUva.query.get(id)
    if not variedad:
        return jsonify({"error": "Variedad no encontrada"}), 404

    return jsonify({
        "id": variedad.id,
        "nombre": variedad.nombre,
        "origen": variedad.origen,
        "foto_ruta": variedad.foto_ruta
    }), 200



#para obtener por html
@variedadUva_bp.route('/listar', methods=['GET']) # Puse '/listar' como ejemplo de URL
def get_variedadesHtml():
    # Obtener todas las variedades de uva de la base de datos como objetos VariedadUva
    variedades = VariedadUva.query.all()  
    
    # Renderiza la plantilla 'variedades.html' y pasa la lista de objetos 'variedades'
    return render_template('/variedades/variedades.html', variedades=variedades), 200

@variedadUva_bp.route('/menu', methods=['GET'])
def menu_variedades():
    return render_template('variedades/menuVariedad.html')


# POST / Crear nueva variedad
@variedadUva_bp.route('/nueva', methods=['POST'])
def crear_variedad():
    nombre = request.form.get('nombre')
    origen = request.form.get('origen')
    foto_ruta = request.files.get('foto_ruta')

    if not nombre:
        return jsonify({"error": "El campo 'nombre' es obligatorio"}), 400
    
    filename = None

    if foto_ruta and foto_ruta.filename != '':
        if allowed_file(foto_ruta.filename):
            filename = secure_filename(foto_ruta.filename)
            image_path = os.path.join(UPLOAD_FOLDER, filename)
            foto_ruta.save(image_path)
        else:
            flash('Formato de imagen no permitido. Solo png, jpg, jpeg, gif.', 'danger')
            return redirect(request.referrer)

    nueva_variedad = VariedadUva(
        nombre=nombre,
        origen=origen,
        foto_ruta=filename
    )

    db.session.add(nueva_variedad)
    db.session.commit()

   
    flash("Variedad creada con éxito", "success")
    return redirect(url_for('variedadUva_bp.get_variedadesHtml')), 201


# PUT / Reemplazar variedad entera
@variedadUva_bp.route('/<string:id>', methods=['PUT'])
def reemplazar_variedad(id):
    variedad = VariedadUva.query.get(id)
    if not variedad:
        return jsonify({"error": "Variedad no encontrada"}), 404

    data = request.get_json()
    if not data or "nombre" not in data:
        return jsonify({"error": "El campo 'nombre' es obligatorio"}), 400

    # Reemplazamos todos los campos
    variedad.nombre = data["nombre"]
    variedad.origen = data.get("origen")
    variedad.foto_ruta = data.get("foto_ruta")

    db.session.commit()

    return jsonify({
        "id": variedad.id,
        "nombre": variedad.nombre,
        "origen": variedad.origen,
        "foto_ruta": variedad.foto_ruta
    }), 200


# PATCH / Modificar parcialmente (opcional)
@variedadUva_bp.route('/<string:id>', methods=['PATCH'])
def modificar_variedad(id):
    variedad = VariedadUva.query.get(id)
    if not variedad:
        return jsonify({"error": "Variedad no encontrada"}), 404

    data = request.get_json()
    if not data:
        return jsonify({"error": "No hay datos para actualizar"}), 400

    # Actualizamos solo campos presentes en data
    if "nombre" in data:
        variedad.nombre = data["nombre"]
    if "origen" in data:
        variedad.origen = data["origen"]
    if "foto_ruta" in data:
        variedad.foto_ruta = data["foto_ruta"]

    db.session.commit()

    return jsonify({
        "id": variedad.id,
        "nombre": variedad.nombre,
        "origen": variedad.origen,
        "foto_ruta": variedad.foto_ruta
    }), 200


# DELETE / Eliminar variedad (solo si no está usada)
@variedadUva_bp.route('/<string:id>', methods=['DELETE'])
def eliminar_variedad(id):
    variedad = VariedadUva.query.get(id)
    if not variedad:
        return jsonify({"error": "Variedad no encontrada"}), 404

    # Verificar si la variedad está asociada a un lote, para no borrarla si está en uso.
    # Como aun no hay relacion se borra directamente 
    # Faltaria implementar relacion con elsmodelo LoteVino para validar si borrar o no
    # Estilo if LoteVino  (no se usa mas esa varieda) se podria borrar.

    db.session.delete(variedad)
    db.session.commit()

    return jsonify({"mensaje": f"Variedad {id} eliminada"}), 200


#metodo para renderizar el formulario de html
@variedadUva_bp.route('/crear', methods=['GET'])
def mostrar_formulario_variedad():
    return render_template('variedades/crear.html') 


@variedadUva_bp.route('/editar/<string:id>', methods=['GET', 'POST'])
def editar_variedad(id):
    variedad = VariedadUva.query.get_or_404(id)

    if request.method == 'POST':
        variedad.nombre = request.form['nombre']
        variedad.origen = request.form['origen']

        foto = request.files.get('foto_ruta')
        if foto and foto.filename != '':
            if allowed_file(foto.filename):
                # Borrar imagen vieja si existe
                if variedad.foto_ruta:
                    old_path = os.path.join(UPLOAD_FOLDER, variedad.foto_ruta)
                    if os.path.exists(old_path):
                        os.remove(old_path)
                # Guardar nueva imagen
                filename = secure_filename(foto.filename)
                path = os.path.join(UPLOAD_FOLDER, filename)
                foto.save(path)
                variedad.foto_ruta = filename
            else:
                flash('Formato de imagen no permitido.', 'danger')
                return redirect(request.referrer)

        db.session.commit()
        flash('Variedad actualizada correctamente.', 'success')
        return redirect(url_for('variedadUva_bp.get_variedadesHtml'))

    return render_template('variedades/editar.html', variedad=variedad)

@variedadUva_bp.route('/delete/<string:id>', methods=['POST'])
def borrar_variedad(id):
    variedad = VariedadUva.query.get_or_404(id)

    # Expira los atributos y relaciones de la instancia para que se recarguen desde la base
    db.session.expire(variedad, ['lotes_vino'])
    db.session.refresh(variedad)

    # Vuelve a consultar si hay lotes asociados
    """if variedad.lotes_vino:
        flash('No se puede eliminar la variedad porque tiene lotes de vino asociados.', 'danger')
        return redirect(url_for('variedadUva_bp.get_variedadesHtml'))"""

    # Borrar imagen si existe
    if variedad.foto_ruta:
        image_path = os.path.join(UPLOAD_FOLDER, variedad.foto_ruta)
        if os.path.exists(image_path):
            os.remove(image_path)

    db.session.delete(variedad)
    db.session.commit()
    flash('Variedad eliminada exitosamente!', 'success')
    return redirect(url_for('variedadUva_bp.get_variedadesHtml'))
