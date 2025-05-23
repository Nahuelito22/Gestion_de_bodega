import uuid
from flask import Blueprint, request, jsonify, abort
from models.variedadUva import VariedadUva
from models.db import db

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


# POST / Crear nueva variedad
@variedadUva_bp.route('/', methods=['POST'])
def crear_variedad():
    data = request.get_json()

    # Validar campos mínimos
    if not data or "nombre" not in data:
        return jsonify({"error": "El campo 'nombre' es obligatorio"}), 400

    nueva_variedad = VariedadUva(
        nombre=data["nombre"],
        origen=data.get("origen"),
        foto_ruta=data.get("foto_ruta")
    )

    db.session.add(nueva_variedad)
    db.session.commit()

    return jsonify({
        "id": nueva_variedad.id,
        "nombre": nueva_variedad.nombre,
        "origen": nueva_variedad.origen,
        "foto_ruta": nueva_variedad.foto_ruta
    }), 201


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
