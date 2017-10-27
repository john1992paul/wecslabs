from flask import Blueprint

teambase = Blueprint('teambase', __name__)

from . import teambase_view