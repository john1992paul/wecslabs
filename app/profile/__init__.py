from flask import Blueprint

profile = Blueprint('profile', __name__)

from . import profilepage
from . import profile_redirect
from . import edit