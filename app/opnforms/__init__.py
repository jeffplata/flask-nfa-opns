from flask import Blueprint

bp = Blueprint('opnforms', __name__)

from app.opnforms import routes
