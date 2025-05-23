import uuid
from flask import Blueprint, request, jsonify
from models.crianza_almacenamiento import CrianzaAlmacenamiento  # importamos el modelo
from models.db import db

# Creamos el blueprint para recepcionUva
crianza_bp = Blueprint('crianza_bp', __name__)