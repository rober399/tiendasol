# modulos/__init__.py
from flask import Blueprint

# Crear un blueprint para el módulo de usuarios
usuarios_bp = Blueprint('usuarios', __name__)

# Importar las rutas de usuarios
from .usuarios import *