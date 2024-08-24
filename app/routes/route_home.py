from flask import Blueprint, render_template
from flask_login import current_user

bp_home = Blueprint('home', __name__)

@bp_home.route('/')
def index():
    return render_template('index.html')