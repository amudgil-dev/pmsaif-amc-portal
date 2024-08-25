from flask import Blueprint, render_template
from flask_login import current_user

bp_home = Blueprint('home', __name__)

# @bp_home.route('/')
# def index():
#     return render_template('index.html')


@bp_home.route('/')
def index():
  print('index()')
  loggedin = 0
  user_name = ""
  is_authenticated = current_user.is_authenticated

  return render_template('index.html',is_authenticated=is_authenticated, user_name=user_name)
#   if current_user.is_authenticated: