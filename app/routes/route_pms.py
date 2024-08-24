from flask import Blueprint, render_template, request,flash,redirect, url_for
from flask_login import login_required, current_user
from app.helpers.queries import getPmsListing
from app.models.models import Transaction
from app.extensions import db
from app.forms.forms import AddTransactionForm
from app.helpers.auth_helper import AuthHelper

bp_pms = Blueprint('pms', __name__)

@bp_pms.route('/pmslist')
@login_required
@AuthHelper.check_session_and_authorize
def pmslist():
  print('pmslist()')
  loggedin = 0
  user_name = ""

  print('getting pms listing...')
  
  print(f"current_user.id = {current_user.id}")
  pms_list = getPmsListing(current_user.id)
  print(pms_list)
  
  # booking_id = db.session.query(Booking).filter(and_(Booking.event_id==event_id, Booking.user_id == uid  )).order_by(Booking.id.desc()).first().id
  
  return render_template('pms_listing.html',
                         loggedin=loggedin, 
                         user_name=user_name,
                         page_heading="List of PMS",
                         pms_list=pms_list)

