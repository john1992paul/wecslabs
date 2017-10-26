from flask import Blueprint

project = Blueprint('project', __name__)

from . import projectmain

from . import project_activity