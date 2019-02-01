from flask import Blueprint

problem = Blueprint('problem', __name__)

from . import views