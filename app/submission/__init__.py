from flask import Blueprint

submission = Blueprint('submission', __name__)

from . import views