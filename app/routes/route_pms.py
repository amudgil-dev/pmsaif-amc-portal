from flask import Blueprint, get_flashed_messages, render_template, request,flash,redirect, url_for
from flask_login import login_required, current_user
from app.helpers.helper_util import enforceAuthz
from app.helpers.queries import getPmsListing, getPmsDashDataList
from app.models.models import Transaction
from app.extensions import db
from app.forms.forms import AddTransactionForm
from app.helpers.auth_helper import AuthHelper
from datetime import date, datetime, timedelta

bp_pms = Blueprint('pms', __name__)

@bp_pms.route('/pmslist')
@login_required
@AuthHelper.check_session_and_authorize
def pmslist():
  print('pmslist()')
  # loggedin = 0
  user_name = ""

  # print('getting pms listing...')
  
  # print(f"current_user.id = {current_user.id}")
  pms_list = getPmsListing(current_user.id)
  # print(pms_list)
  
    
  # loggedin,user_name = get_user_status()
  
  print(f" current_user details: {current_user}")
  
  return render_template('pms_listing.html',
                        #  loggedin=loggedin, 
                         is_authenticated = current_user.is_authenticated,
                         user_name= current_user.fname + " " + current_user.lname,
                         page_heading="List of PMS",
                         pms_list=pms_list)


# def get_user_status():
#   if current_user.is_authenticated:
#       loggedin = 1
#       user_name = current_user.fname + " " + current_user.lname

#       return loggedin, user_name
#   else:
#       return 0, "BHOLA"


@bp_pms.route('/pmsdash/<int:pms_id>')
@login_required
@AuthHelper.check_session_and_authorize
def pms_dashboard(pms_id):
  print('pms_dashboard()')

  # loggedin,user_name = get_user_status()
  # if loggedin == 0:
  #     return redirect(url_for('users.logout'))
  

  
  # print("AuthZ PASSED and proceeding ...")
  get_flashed_messages()
  
  pms,index_perf,pms_details,pms_stocks, pms_sectors = getPmsDashDataList(pms_id)  

  print('--- BEFORE ROUTE ---')
  print(pms.one_month)
  print(pms.pms_id)
  print('--- JUST BEFORE ROUTE ---')
  
  # booking_id = db.session.query(Booking).filter(and_(Booking.event_id==event_id, Booking.user_id == uid  )).order_by(Booking.id.desc()).first().id
  temp_date  = datetime(pms.year, pms.month, 1)
  date_display = temp_date.strftime("%B, %Y")

  return render_template('pms_dashboard.html',
                         is_authenticated = current_user.is_authenticated,
                         user_name= current_user.fname + " " + current_user.lname,
                         page_heading="PMS Dashboard - "+pms.pms_name,
                         pms=pms,
                         date_display=date_display,
                         index=index_perf,
                         pms_details=pms_details,
                         pms_stocks=pms_stocks,
                         pms_sectors=pms_sectors
                         )