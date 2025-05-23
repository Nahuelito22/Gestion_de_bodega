import uuid
from flask import Blueprint, request, jsonify
from models.recepcionUva import RecepcionUva  # importamos el modelo
from models.db import db

# Creamos el blueprint para recepcionUva
recepcionUva_bp = Blueprint('recepcionUva_bp', __name__)