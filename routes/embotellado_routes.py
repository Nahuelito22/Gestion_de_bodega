import uuid
from flask import Blueprint, request, jsonify
from models.embotellado import Embotellado  # importamos el modelo
from models.db import db

# Creamos el blueprint para recepcionUva
embotellado_bp = Blueprint('embotellado_bp', __name__)