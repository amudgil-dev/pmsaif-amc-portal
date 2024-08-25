from sqlite3 import IntegrityError
from flask import Blueprint, get_flashed_messages, render_template, request,flash,redirect, url_for
from flask_login import login_required, current_user
from app.helpers.helper_util import enforceAuthz, get_missing_months, getLastMonthYYMM
from app.helpers.queries import getPmsListing, getPmsDashDataList, getPmsNavDataList
from app.models.models import AMCMaster, PMSMaster, PMSNav, PMSPerformance, Transaction
from app.extensions import db
from app.forms.forms import AddTransactionForm, DummyForm, NavForm, PMSMasterEditForm, PMSPerformanceEditForm, PMSPerformanceForm
from app.helpers.auth_helper import AuthHelper
from datetime import date, datetime, timedelta

bp_nav = Blueprint('nav', __name__)

@bp_nav.route('/pmsnav/<int:pms_id>')
@login_required
@AuthHelper.check_session_and_authorize
def pms_nav_dashboard(pms_id):
  print('pms_nav_dashboard()')

  
  pms, pms_nav = getPmsNavDataList(pms_id)  

  print('--- BEFORE ROUTE ---')
  print(pms_nav.p_month)
  print(pms_nav.p_year)
  print(pms_nav.nav)
  print('--- JUST BEFORE ROUTE ---')
  
  # booking_id = db.session.query(Booking).filter(and_(Booking.event_id==event_id, Booking.user_id == uid  )).order_by(Booking.id.desc()).first().id
  temp_date  = datetime(pms_nav.p_year, pms_nav.p_month, 1)
  date_display = temp_date.strftime("%B, %Y")

  return render_template('pms_nav_dashboard.html',
                         is_authenticated = current_user.is_authenticated,
                         user_name= current_user.fname + " " + current_user.lname,
                         page_heading="PMS NAV Dashboard - "+pms.pms_name,
                         pms=pms,
                         date_display=date_display,
                         pms_details=pms_details,
                         pms_stocks=pms_stocks,
                         pms_sectors=pms_sectors
                         )
  
# Route to display NAV entries for a given PMS_ID
@bp_nav.route('/pms_nav/<int:pms_id>')
@login_required
@AuthHelper.check_session_and_authorize
def pms_nav_list(pms_id):
    print('pms_nav_list()')
    
    pms = PMSMaster.query.filter_by(pms_id=pms_id).first()
    # print(pms.name)
    navs = PMSNav.query.filter_by(pms_id=pms_id).order_by(PMSNav.p_year.desc(), PMSNav.p_month.desc()).all()
    return render_template('pms_nav_list.html',
                          is_authenticated = current_user.is_authenticated,
                          user_name= current_user.fname + " " + current_user.lname,                           
                          page_heading="PMS NAV History ",
                          pms=pms, pms_id=pms_id, 
                          navs=navs)

# Route to add or edit a NAV entry
@bp_nav.route('/pms_nav/<int:pms_id>/edit/<int:year>/<int:month>', methods=['GET', 'POST'])
@login_required
@AuthHelper.check_session_and_authorize
def edit_nav(pms_id, year, month):
    
        
    pms = PMSMaster.query.filter_by(pms_id=pms_id).first()
    
    if pms is None:
        print("{pms.name}")
    
    print(pms.name)
        
    nav = PMSNav.query.filter_by(pms_id=pms_id, p_year=year, p_month=month).first()
    print(nav)
    if nav is None:
        nav = PMSNav(pms_id=pms_id, p_year=year, p_month=month)

    form = NavForm(obj=nav)
    
    if form.validate_on_submit():
        form.populate_obj(nav)
        db.session.add(nav)
        db.session.commit()
        flash('NAV entry updated successfully', 'success')
        return redirect(url_for('nav.pms_nav_list',
                                pms_id=pms_id))

    return render_template('pms_nav_edit.html', 
                          is_authenticated = current_user.is_authenticated,
                          user_name= current_user.fname + " " + current_user.lname,                                  
                          form=form, 
                          page_heading="EDIT PMS NAV ",
                          pms_id=pms_id, 
                          pms=pms, 
                          year=year, 
                          month=month, 
                          nav=nav)

# Route to add missing NAV entries
@bp_nav.route('/pms_nav/<int:pms_id>/add_missing', methods=['GET', 'POST'])
@login_required
@AuthHelper.check_session_and_authorize
def add_missing_nav(pms_id):
    
    form = DummyForm()

    current_date = datetime.now()
    
    missing_entries = []
    
    pms = PMSMaster.query.filter_by(pms_id=pms_id).first()
    print(pms.name)
        
    navs = PMSNav.query.filter_by(pms_id=pms_id).order_by(PMSNav.p_year.desc(), PMSNav.p_month.desc()).all()
    
    print(current_date.year, current_date.month)
    print(type(navs))
    
    oldest = navs[-1]
    latest = navs[0]
    print(oldest.p_year, oldest.p_month,)
    print(latest.p_year, latest.p_month,)
    
    existing_data = [(nav.p_year, nav.p_month) for nav in navs]
 
    
    missing_entries =  get_missing_months(existing_data)

    print(' printing possible entries')
    for entries in missing_entries:
        print(entries)

    if request.method == 'POST':
        if form.validate_on_submit(): 
            for year, month in missing_entries:
                nav = request.form.get(f'nav_{year}_{month}')
                if nav:
                    new_nav = PMSNav(pms_id=pms_id, p_year=year, p_month=month, nav=float(nav),user_id=current_user.id,   created_at=datetime.now())
                    db.session.add(new_nav)
            
            db.session.commit()
            flash('Missing NAV entries added successfully', 'success')
            return redirect(url_for('nav.pms_nav_list', pms_id=pms_id))
        flash('Missing NAV entries could not be added ', 'warning') 
        return redirect(url_for('nav.pms_nav_list', pms_id=pms_id))        

    
    return render_template('pms_nav_add_missing.html', 
                            is_authenticated = current_user.is_authenticated,
                            user_name= current_user.fname + " " + current_user.lname,                              
                            page_heading="Add Missing NAV Data",
                            pms_id=pms_id, 
                            pms =pms,
                            form = form,
                            missing_entries=missing_entries)



