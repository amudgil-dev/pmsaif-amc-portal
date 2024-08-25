from sqlite3 import IntegrityError
from flask import Blueprint, get_flashed_messages, render_template, request,flash,redirect, url_for
from flask_login import login_required, current_user
from app.helpers.helper_util import enforceAuthz, getLastMonthYYMM
from app.helpers.queries import getPmsListing, getPmsDashDataList
from app.models.models import AMCMaster, PMSMaster, PMSPerformance, Transaction
from app.extensions import db
from app.forms.forms import AddTransactionForm, PMSMasterEditForm, PMSPerformanceEditForm, PMSPerformanceForm
from app.helpers.auth_helper import AuthHelper
from datetime import date, datetime, timedelta

bp_pms = Blueprint('pms', __name__)

@bp_pms.route('/pmslist')
@login_required
@AuthHelper.check_session
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
@AuthHelper.check_session
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
  



@bp_pms.route('/editpms/<int:pms_id>', methods=['GET', 'POST'])
@login_required
@AuthHelper.check_session
def edit_pms(pms_id):
  print('in edit_pms()()')


  pms = PMSMaster.query.filter_by(pms_id=pms_id).first()
  # if pms is None:
  #   flash('Not Authorised, please contat PMSAIF Administrator!', 'danger')
  #   print('PMs not found not valid')
  #   return redirect(url_for('pmslist'))

  pms.large_cap = "%.2f"%pms.large_cap
  pms.mid_cap = "%.2f"%pms.mid_cap
  pms.small_cap = "%.2f"%pms.small_cap
  pms.cash = "%.2f"%pms.cash
  
  # print('pms found')
  pms_name = pms.name
  form = PMSMasterEditForm(obj=pms)
  # print( "{:.2f}".format(form.large_cap))

  # print(pms.amc_id)

  amc = AMCMaster.query.filter_by(amc_id=pms.amc_id).first()

  if request.method == 'GET':
      return render_template('form_edit_pms_master.html', 
                                is_authenticated = current_user.is_authenticated,
                                user_name= current_user.fname + " " + current_user.lname,
                                page_heading="Change PMS Details - "+pms_name,                         
                                form=form,
                                amc=amc,
                                pms= pms
                                )

  if request.method == 'POST':
    print('in post')
    # print(pms.pms_id,pms.name, pms.amc_id, pms.aum, pms.stocks_min, pms.stocks_max, pms.portfolio_pe, pms.large_cap, pms.mid_cap, pms.small_cap, pms.cash)
    # print(' -----')

    if form.validate_on_submit():
      pms.aum = form.aum.data
      pms.stocks_min = form.stocks_min.data
      pms.stocks_max = form.stocks_max.data
      pms.portfolio_pe = form.portfolio_pe.data
      pms.large_cap = form.large_cap.data
      pms.mid_cap = form.mid_cap.data
      pms.small_cap = form.small_cap.data
      pms.cash = form.cash.data


      try:
         
        db.session.commit()
      except Exception as e:
        print('Exception occured while updating PMS details')
        print(e)
        db.session.rollback()
        flash('PMS details could not be updated, please try again!', 'danger')
        
        return redirect(url_for('pms.pms_dashboard', pms_id=pms_id))
      # return redirect('../pmsdash/'+str(pms.pms_id))
    

      flash('PMS details updated successfully!', 'success')
      # return redirect('../pmsdash/'+str(pms.pms_id))
      return redirect(url_for('pms.pms_dashboard', pms_id=pms_id))
    else:
      print(form.errors)
      flash('Event could not be updated!', 'danger')
      flash(form.errors, 'danger')
      return redirect(url_for('pms.pms_dashboard', pms_id=pms_id))




@bp_pms.route('/editpmsperf/<int:pms_id>', methods=['GET', 'POST'])
@login_required
@AuthHelper.check_session
def edit_pmsperf(pms_id):
  print('in edit_pmsperf()')

  
  pms = PMSMaster.query.filter_by(pms_id=pms_id).first()
  # if pms is None:
  #   flash('Not Authorised, please contat PMSAIF Administrator!', 'danger')
  #   print('PMs not found not valid')
  #   return redirect(url_for('pms.pmslist'))

  # print('pms found')
  pms_name = pms.name

  # print(pms.amc_id)

  amc = AMCMaster.query.filter_by(amc_id=pms.amc_id).first()

  pms_perf = PMSPerformance.query.filter_by(pms_id=pms_id).order_by(PMSPerformance.id.desc()).first()

  print(pms_perf.p_month)
  print(pms_perf)
  form = PMSPerformanceEditForm(obj=pms_perf)
  print(' ------- perf is out -----')
  
  if request.method == 'GET':
      return render_template('form_edit_pms_performance.html', 
                                is_authenticated = current_user.is_authenticated,
                                user_name= current_user.fname + " " + current_user.lname,
                                page_heading="Change PMS Performance  - "+pms_name,                         
                                form=form,
                                amc=amc,
                                pms= pms
                                )

  if request.method == 'POST':
    print('in post')
    # print(pms_perf.one_month,pms_perf.three_month,pms_perf.six_month,pms_perf.one_year,pms_perf.three_year,pms_perf.five_year,pms_perf.ten_year,pms_perf.cagr_si,pms_perf.si,pms_perf.created_at)
    print(' -----')

    if form.validate_on_submit():
      pms_perf.one_month = form.one_month.data
      pms_perf.three_months = form.three_months.data
      pms_perf.six_months = form.six_months.data
      pms_perf.twelve_months = form.twelve_months.data
      pms_perf.two_year_cagr = form.two_year_cagr.data      
      pms_perf.three_year_cagr = form.three_year_cagr.data
      pms_perf.five_year_cagr = form.five_year_cagr.data
      pms_perf.ten_year_cagr = form.ten_year_cagr.data
      pms_perf.cagr_si = form.cagr_si.data
      pms_perf.si = form.si.data


      try:
         
        db.session.commit()
      except Exception as e:
        print('Exception occured while updating PMS details')
        print(e)
        db.session.rollback()
        flash('PMS Performance details could not be updated, please try again!', 'danger')
        return redirect(url_for('pms.pms_dashboard', pms_id=pms_id))
    

      flash('PMS details updated successfully!', 'success')
      return redirect('../pmsdash/'+str(pms.pms_id))
    else:
      print(form.errors)
      flash('Event could not be updated!', 'danger')
      flash(form.errors, 'danger')
      return redirect(url_for('pms.pms_dashboard', pms_id=pms_id))
    



@bp_pms.route('/newpmsperf/<int:pms_id>', methods=['GET', 'POST'])
@login_required
@AuthHelper.check_session
def new_pmsperf(pms_id):
  print('in new_pmsperf()')

  # loggedin,user_name = get_user_status()
  # if loggedin == 0:
  #   flash('Please login to continue!', 'danger')
  #   print('login is not valid')
  #   return redirect(url_for('users.logout'))
  
  # # if userEntitledToChange(current_user.id,pms_id) == False:
  # #   flash('You are not authorised to change this PMS, please contat PMSAIF Administrator!', 'danger')
  # #   print('Authorization not valid')
  # #   # return redirect(url_for('pmslist'))
  # #   return redirect(url_for('pms_dashboard', pms_id=pms_id))
  
  # if not enforceAuthz(pms_id):
  #   print('AuthZ Failed and redirecting')
  #   return redirect(url_for('pms.pms_dashboard',pms_id=pms_id))
  
  # form = PMSMasterForm()
      # load the event from the database
  get_flashed_messages() # Clear Flash Message
  pms = PMSMaster.query.filter_by(pms_id=pms_id).first()
  # if pms is None:
  #   flash('Not Authorised, please contat PMSAIF Administrator!', 'danger')
  #   print('PMs not found not valid')
  #   # return redirect(url_for('pmslist'))
  #   return redirect(url_for('pms.pms_dashboard', pms_id=pms_id))    

  # print('pms found')
  pms_name = pms.name

  # print(pms.amc_id)

  amc = AMCMaster.query.filter_by(amc_id=pms.amc_id).first()

  # pms_perf = PMSPerformance.query.filter_by(pms_id=pms_id).order_by(PMSPerformance.id.desc()).first()

  # print(pms_perf.p_month)
  # print(pms_perf)
  form = PMSPerformanceForm()
  print(' ------- perf is out -----')

  year, prev_month = getLastMonthYYMM()

  form.p_month.data = prev_month
  form.p_year.data = year
  
  temp_date  = datetime(int(year), int(prev_month), 1)
  date_display = temp_date.strftime("%B, %Y")

  if request.method == 'GET':
      return render_template('form_create_pms_performance.html', 
                                is_authenticated = current_user.is_authenticated,
                                user_name= current_user.fname + " " + current_user.lname,
                                page_heading="Add PMS Performance  - "+pms_name,       
                                date_display = date_display,         
                                form=form,
                                amc=amc,
                                pms= pms
                                )

  if request.method == 'POST':
    print('in post')
    # print(pms_perf.one_month,pms_perf.three_month,pms_perf.six_month,pms_perf.one_year,pms_perf.three_year,pms_perf.five_year,pms_perf.ten_year,pms_perf.cagr_si,pms_perf.si,pms_perf.created_at)
    print(' -----')

    if form.validate_on_submit():
      print('form validated')
      new_record = PMSPerformance (
          pms_id=pms.pms_id,
          user_id=current_user.id,
          p_month=prev_month,
          p_year=year,

          one_month=form.one_month.data,
          three_months=form.three_months.data,
          six_months=form.six_months.data,
          twelve_months=form.twelve_months.data,
          two_year_cagr=form.two_year_cagr.data,
          three_year_cagr=form.three_year_cagr.data,
          five_year_cagr=form.five_year_cagr.data,
          ten_year_cagr=form.ten_year_cagr.data,
          cagr_si=form.cagr_si.data,
          si=form.si.data,
          created_at=datetime.now()
      )
      
      print('form.si.data =>',form.si.data)
      print('form.cagr_si.data =>',form.cagr_si.data)      

      print(new_record)
      print('------------ record to be saved ----------')
      # Add the new event to the database
      try:
          
        db.session.add(new_record)
        db.session.commit()

        # print(' ------- new performance committed ----------')

        flash("PMS Performance saved,!",'success')
        return redirect('/pmslist')
      
      except IntegrityError as exc:
        print('Integrity Error occured!!!')
        print(exc)
        db.session.rollback()
        flash("Performance data for this period already exist, please change rather than add!",'danger')
        # form = editPostForm(form)
        # return redirect('/pmslist')
        return redirect(url_for('pms.pms_dashboard', pms_id=pms_id))
      
      except Exception as e:
        print('something went wrong!!!')
        print(e)
        db.session.rollback()
        flash("Performance data for this period already exist, please change rather than add!",'danger')
        # form = editPostForm(form)
        # return redirect('/pmslist')
        return redirect(url_for('pms.pms_dashboard', pms_id=pms_id))
        


    else:
        print('form validation failed')
        print(form.errors)
        flash(form.errors,'danger')
        # return redirect('/pmslist')
        return redirect(url_for('pms.pms_dashboard', pms_id=pms_id))
        # Process the data as needed (e.g., store in a database)

