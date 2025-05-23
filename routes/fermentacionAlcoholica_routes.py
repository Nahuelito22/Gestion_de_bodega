import uuid
from flask import Blueprint, request, jsonify
from models.fermentacionAlcoholica import FermentacionAlcoholica  # importamos el modelo
from models.db import db

# Creamos el blueprint para recepcionUva
fermentacion_bp = Blueprint('fermentacion_bp', __name__)