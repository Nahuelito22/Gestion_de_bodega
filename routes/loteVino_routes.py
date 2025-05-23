import uuid
from flask import Blueprint, request, jsonify
from models.loteVino import LoteVino  # importamos el modelo
from models.db import db

# Creamos el blueprint para LoteVino
loteVino_bp = Blueprint('loteVino_bp', __name__)