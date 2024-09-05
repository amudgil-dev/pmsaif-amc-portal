import calendar
from datetime import datetime
# from sqlite3 import IntegrityError
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from flask import Blueprint, render_template, redirect, send_file, url_for, flash,current_app,request
from flask_login import login_user, logout_user, login_required, current_user
from markupsafe import Markup
from app.helpers.helper_excel import write_Excel_report
from app.helpers.helper_util import generate_resetlink,email_resetlink, getLastMonthYYMM, isAdmin
from app.helpers.queries import getAdminPmsListingByIndex, getIndexListing, getIndexPerformance, getPerformanceReport,getAmcListing,getAdminPmsListing, getUserListing
from app.models.models import AMCMaster, IndexMaster, IndexPerformance, User, UserRole
from app.forms.forms import DummyForm, IndexPerformanceEditForm, IndexPerformanceForm, ResetPasswordForm, ResetRequestForm, SigninForm, SignupForm
from app.helpers.auth_helper import AuthHelper
from app.helpers.logging_helper import debug, info, warning, error, critical, log_exception, log_function_call
from app.extensions import login_manager, db

bp_admin = Blueprint('admin', __name__)



@bp_admin.route('/admin')
@login_required
@AuthHelper.check_session
@AuthHelper.check_pms_authorisations
def admin_home():
  print('admin_home()')
  # loggedin = 0
  user_name = ""

  # print('getting pms listing...')
  
  # print(f"current_user.id = {current_user.id}")
  amc_list = getAmcListing()
  # print(pms_list)
  if is_empty(amc_list):
    return redirect(url_for('admin.admin_home'))
  
  return render_template('admin_amc_listing.html',
                         is_authenticated = current_user.is_authenticated,
                         is_admin=isAdmin(current_user.userrole_id),                         
                         user_name= current_user.fname + " " + current_user.lname,
                         page_heading="List of AMC",
                         amc_list=amc_list)




@bp_admin.route('/indexlist')
@login_required
@AuthHelper.check_session
@AuthHelper.check_admin_authorisations
def index_list():
  # print('index_list()')

      
  index_list = getIndexListing()
  if is_empty(index_list):
    return redirect(url_for('admin.admin_home'))
    
  return render_template('admin_index_listing.html',
                         is_authenticated = current_user.is_authenticated,
                         is_admin=isAdmin(current_user.userrole_id),                         
                         user_name= current_user.fname + " " + current_user.lname,
                         page_heading="List of Index",
                         index_list=index_list)


@bp_admin.route('/viewindexperf/<int:index_id>')
@login_required
@AuthHelper.check_session
@AuthHelper.check_admin_authorisations
def view_indexperf(index_id):
  print('view_indexperf()')
      
  index_perf = getIndexPerformance(index_id)
  # print('back in function')
  if is_empty(index_perf):
    return redirect(url_for('admin.admin_home'))
    

  return render_template('admin_index_perf.html',
                         is_authenticated = current_user.is_authenticated,
                         is_admin=isAdmin(current_user.userrole_id),                         
                         user_name= current_user.fname + " " + current_user.lname,
                         page_heading="Index Performance - History",
                         index_perf=index_perf)




@bp_admin.route('/editindexperf/<int:index_id>', methods=['GET', 'POST'])
@login_required
@AuthHelper.check_session
@AuthHelper.check_admin_authorisations
def edit_indexperf(index_id):
  print('in edit_indexperf()')

  index_perf = IndexPerformance.query.filter_by(id=index_id).order_by(IndexPerformance.id.desc()).first()
  # index_perf_list = [index_perf] if index_perf else []
  
  if is_empty(index_perf):
    return redirect(url_for('admin.edit_indexperf', index_id=index_id))
  
  index = IndexMaster.query.filter_by(id=index_perf.index_id).first()


  # print(index_perf.p_month)
  # print(index_perf)
  form = IndexPerformanceEditForm(obj=index_perf)
  # print(' ------- perf is out -----')
  
  if request.method == 'GET':
      return render_template('admin_form_edit_index_performance.html', 
                                is_authenticated = current_user.is_authenticated,
                                is_admin=isAdmin(current_user.userrole_id),                                
                                user_name= current_user.fname + " " + current_user.lname,
                                page_heading="Change Index Performance  - "+index.name,                         
                                form=form
                                )

  if request.method == 'POST':

    # print('in post')
    # print(index_perf.one_month,index_perf.three_month,index_perf.six_month,index_perf.one_year,index_perf.three_year,index_perf.five_year,index_perf.ten_year,index_perf.cagr_si,index_perf.si,index_perf.created_at)
    # print(' -----')

    if form.validate_on_submit():
      index_perf.one_month = form.one_month.data
      index_perf.three_months = form.three_months.data
      index_perf.six_months = form.six_months.data
      index_perf.twelve_months = form.twelve_months.data
      index_perf.two_year_cagr = form.two_year_cagr.data      
      index_perf.three_year_cagr = form.three_year_cagr.data
      index_perf.five_year_cagr = form.five_year_cagr.data
      index_perf.ten_year_cagr = form.ten_year_cagr.data
      # index_perf.cagr_si = form.cagr_si.data
    

      try:
         
        db.session.commit()
      except Exception as e:
        # print('Exception occured while updating PMS details')
        print(e)
        db.session.rollback()
        flash('Index Performance details could not be updated, please try again!', 'danger')
        return redirect(url_for('admin.view_indexperf',index_id=index_perf.index_id))
    

      flash('Index Performance updated successfully!', 'success')
      return redirect(url_for('admin.view_indexperf',index_id=index_perf.index_id))
    else:
      print(form.errors)
      flash('Index Perfromance could not be updated!', 'danger')
      flash(form.errors, 'danger')
      return redirect(url_for('admin.view_indexperf',index_id=index_perf.index_id))



@bp_admin.route('/newindexperf/<int:index_id>', methods=['GET', 'POST'])
@login_required
@AuthHelper.check_session
@AuthHelper.check_admin_authorisations
def new_indexperf(index_id):
  # print('in new_indexperf()')

  index = index = IndexMaster.query.filter_by(id=index_id).first()

  if index is None:
    flash('Not Authorised, please contat PMSAIF Administrator!', 'danger')
    # print('Index Id not found not valid')
    return redirect(url_for('admin.admin_home'))
  
  
  form = IndexPerformanceForm()

  year, prev_month = getLastMonthYYMM()

  form.p_month.data = prev_month
  form.p_year.data = year
  
  temp_date  = datetime(int(year), int(prev_month), 1)
  date_display = temp_date.strftime("%B, %Y")

  if request.method == 'GET':
      return render_template('admin_form_create_index_performance.html', 
                                is_authenticated = current_user.is_authenticated,
                                is_admin=isAdmin(current_user.userrole_id),                                
                                user_name= current_user.fname + " " + current_user.lname,
                                page_heading="Add Index Performance  - "+index.name,       
                                date_display = date_display,         
                                form=form
                                )


  if request.method == 'POST':
    # print('in post')
    # print(pms_perf.one_month,pms_perf.three_month,pms_perf.six_month,pms_perf.one_year,pms_perf.three_year,pms_perf.five_year,pms_perf.ten_year,pms_perf.cagr_si,pms_perf.si,pms_perf.created_at)
    # print(' -----')

    if form.validate_on_submit():
      # print('form validated')
      new_record = IndexPerformance (
          index_id=index.id,
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

        
          created_at=datetime.now()
      )

      # print(new_record)
      # print('------------ record to be saved ----------')
      # Add the new event to the database
      try:
          
        db.session.add(new_record)
        db.session.commit()

        # print(' ------- new performance committed ----------')

        flash("Index Performance saved,!",'success')
        return redirect(url_for('admin.view_indexperf', index_id=index.id))
      
      except IntegrityError as exc:
        print('Integrity Error occured!!!')
        db.session.rollback()
        flash("Performance data for this period already exist, please change rather than add!",'danger')
        # form = editPostForm(form)
        # return redirect('/pmslist')
        return redirect(url_for('admin.view_indexperf', index_id=index.id))
      
      except Exception as e:
        print('something went wrong!!!')
        db.session.rollback()
        flash("Performance data for this period already exist, please change rather than add!",'danger')
        # form = editPostForm(form)
        # return redirect('/pmslist')
        return redirect(url_for('admin.view_indexperf', index_id=index.id))
        


    else:
        print('form validation failed')
        print(form.errors)
        flash(form.errors,'danger')
        # return redirect('/pmslist')
        return redirect (url_for('admin.new_indexperf', index_id=index_id))
        # Process the data as needed (e.g., store in a database)




@bp_admin.route('/admin/<int:amc_id>')
@login_required
@AuthHelper.check_session
@AuthHelper.check_admin_authorisations
def admin_pmslist(amc_id):
  # print('admin_pmslist()')
  # print(f"amc_id = {amc_id}")
  pms_list = getAdminPmsListing(amc_id)
  # print(pms_list)
  if is_empty(pms_list):
    return redirect(url_for('admin.admin_home'))

  
  return render_template('pms_listing.html',
                         is_authenticated = current_user.is_authenticated,
                         is_admin=isAdmin(current_user.userrole_id),                         
                         user_name= current_user.fname + " " + current_user.lname,
                         page_heading="List of PMS",
                         pms_list=pms_list)


@bp_admin.route('/admin/users/<int:amc_id>')
@login_required
@AuthHelper.check_session
@AuthHelper.check_admin_authorisations
def admin_userlist(amc_id):
  print('admin_userlist()')
  # print(f"amc_id = {amc_id}")
  user_list = getUserListing(amc_id)
  # print(user_list)
  amc_record = AMCMaster.query.filter_by(amc_id=amc_id).first()
  
  print(f"amc_record ==> {amc_record} and type = {type(amc_record)}")
  
  if amc_record is None:
    flash (' Not found, contact administrator! ', 'warning')
    return redirect('/admin')
  
  return render_template('admin_amc_user_listing.html',
                         is_authenticated = current_user.is_authenticated,
                         is_admin=isAdmin(current_user.userrole_id),                         
                         user_name= current_user.fname + " " + current_user.lname,
                         page_heading="List of AMC Users",
                         amc_name = amc_record.name,
                         amc_id=amc_id,
                         user_list=user_list)



# create User for an AMC
# @app.route('/register', methods=['GET','POST'])
# @app.route('/signup', methods=['GET','POST'])
@bp_admin.route('/admin/register/<int:amc_id>', methods=['GET','POST'])
@login_required
@AuthHelper.check_session
@AuthHelper.check_admin_authorisations
  
def user_registeration(amc_id):
  print('in user_registeration()')
  name = None
  email = None
  form = SignupForm()
  
  amc_record = AMCMaster.query.filter_by(amc_id=amc_id).first()

  if request.method=="POST":
    # Validate form
    if form.validate_on_submit():

      fname = form.fname.data.strip()
      lname = form.lname.data.strip()
      email = form.email.data.strip()
      # password = form.password_hash.data.strip()

      # Making it safe against XSS attacks
      fname = Markup.escape(fname )
      lname = Markup.escape(lname )      
      email = Markup.escape(email )


      print(fname, email)
      isactive = 0
      user_role = db.session.query(UserRole).filter(UserRole.name=="SUBMITTER").first().id

        
      newUser = User(fname=fname,lname=lname, email=email, amc_id=amc_id, password="11111", userrole_id=user_role,isactive=1,created_at=datetime.now())

      try:
        print(' Before adding the user to the session...')
        print(f"user = {newUser}")
        db.session.add(newUser)
        db.session.commit()
        # # logging user registration 
        # log_txn(msgType='REGISTER', log_desc='Registered user', user_id=newUser.id, booking_id=None, event_id=None, ticket_id=None, created_at=None)  

        # # sending email notification for activation 
        # link = generate_act_activation_link (newUser)
        # email_list = []
        # email_list.append(email)
        # send_email_for_activation(link, email_list)



        # # logging sending of notification
        # log_txn(msgType='EMAIL_NOTIFICATION', log_desc='Welcome Email Sent', user_id=newUser.id, booking_id=None, event_id=None, ticket_id=None, created_at=None)          
        # flash("User created Successfully! You can browse but to book tickets you need to activate account.Please follow instructions sent to your email for activating your account!", 'warning')

        # # forcing the user to login after this activity
        # logout_user()
        # pop_user_in_session(session)

        # return redirect('/admin/<int:amc_id>')
        return redirect('/admin/users/'+str(amc_id))
      
      except SQLAlchemyError as exc:
       print('Integrity Error occured!!!')
       db.session.rollback()
       flash("EmailId is already registered, login/reset password or register with another email !",'danger')
      #  log_txn(msgType='REGISTER_FAILURE', log_desc='Email Already Registered ', user_id=None, booking_id=None, event_id=None, ticket_id=None, created_at=None) 
    #   form.name.data = ''
    #   form.email.data = ''      
    else:
      # print('Validation failed ')
      # print(form.errors )
      flash(form.errors, 'danger')
      # log_txn(msgType='FORM_FAILURE', log_desc='Registeration form validation failed ', user_id=None, booking_id=None, event_id=None, ticket_id=None, created_at=None) 
    
    print(' Returning the form back ...')
    return render_template("form_signup.html", 
                         is_authenticated = current_user.is_authenticated,
                         is_admin=isAdmin(current_user.userrole_id),                         
                         user_name= current_user.fname + " " + current_user.lname,
                         page_heading="Create AMC User",
                         amc_name = amc_record.name,     
                              form= form)

  if request.method=="GET":
   
   form.fname.data = ''
   form.lname.data = ''
   form.email.data = '' 
   return render_template("form_signup.html", 
                         is_authenticated = current_user.is_authenticated,
                         is_admin=isAdmin(current_user.userrole_id),                         
                         user_name= current_user.fname + " " + current_user.lname,
                         page_heading="Create AMC User",
                         amc_name = amc_record.name,                          
                          # name = name,
                          # email= email,
                          form= form)


@bp_admin.route('/admin/users/delete/<int:user_id>')
@login_required
@AuthHelper.check_session
@AuthHelper.check_admin_authorisations
def admin_delete_user(user_id):
  print('admin_delete_user()')
  
  user = User.query.filter_by(id=user_id).first()
  
  if user:
    amc_id = user.amc_id
    # print(f"amc_id = {amc_id}")
    
    # Delete the user
    db.session.delete(user)
    db.session.commit()
  else:
      print("User not found")
  
  return redirect('/admin/users/'+str(amc_id))
  




@bp_admin.route('/admin/users/edit/<int:user_id>', methods=['GET','POST'])
@login_required
@AuthHelper.check_session
@AuthHelper.check_admin_authorisations
def admin_edit_user(user_id):
  print('admin_edit_user()')
  
  user = User.query.filter_by(id=user_id).first()
  
  amc_id = user.amc_id
  amc_record = AMCMaster.query.filter_by(amc_id=amc_id).first()
  
  form = SignupForm()
  
  if request.method == 'GET':
      form.fname.data = user.fname
      form.lname.data = user.lname
      form.email.data = user.email
      
      return render_template('form_edit_user.html', 
                              is_authenticated = current_user.is_authenticated,
                              is_admin=isAdmin(current_user.userrole_id),      
                              user_name= current_user.fname + " " + current_user.lname,
                              page_heading="Change User Details",    
                              amc_name = amc_record.name,                     
                              form=form
                              )

      
  if request.method == 'POST':
    print('in post')
    # print(pms.pms_id,pms.name, pms.amc_id, pms.aum, pms.stocks_min, pms.stocks_max, pms.portfolio_pe, pms.large_cap, pms.mid_cap, pms.small_cap, pms.cash)
    # print(' -----')

    if form.validate_on_submit():
      print('form validated')
      user.fname = form.fname.data
      user.lname = form.lname.data
      user.email = form.email.data


      try:
         
        db.session.commit()
      except Exception as e:
        print('Exception occured while updating PMS details')
        print(e)
        db.session.rollback()
        flash('PMS details could not be updated, please try again!', 'danger')
        
        
        return redirect('/admin/users/'+str(amc_id))
      # return redirect('../pmsdash/'+str(pms.pms_id))
    

      flash('PMS details updated successfully!', 'success')
      # return redirect('../pmsdash/'+str(pms.pms_id))
      return redirect('/admin/users/'+str(amc_id))
    else:
      print(form.errors)
      flash('Event could not be updated!', 'danger')
      flash(form.errors, 'danger')
      return redirect('/admin/users/'+str(amc_id))
  
  return redirect('/admin/users/'+str(amc_id))

 
@bp_admin.route('/admin/index/<int:index_id>')
@login_required
@AuthHelper.check_session
@AuthHelper.check_admin_authorisations
def admin_pmslist_by_index(index_id):
  print('admin_pmslist_by_index()')
  print(f"index_id = {index_id}")
  pms_list = getAdminPmsListingByIndex(index_id)
  # print(pms_list)
  
  
  if is_empty(pms_list):
    return redirect(url_for('admin.admin_home'))
    
  # loggedin,user_name = get_user_status()
  
  # print(f" current_user details: {current_user}")
  
  return render_template('pms_listing_for_index.html',
                         is_authenticated = current_user.is_authenticated,
                         is_admin=isAdmin(current_user.userrole_id),                         
                         user_name= current_user.fname + " " + current_user.lname,
                         page_heading="List of PMS",
                         pms_list=pms_list)
  
def is_empty(data_list, redirect_url='admin.admin_home', flash_message='No data found. Redirecting to home.'):
  
  if isinstance(data_list, list):
      if data_list is None or len(data_list) == 0:
        flash(flash_message, 'warning')
        return redirect(url_for(redirect_url))
      return False
  else:
    if data_list is None:
      flash(flash_message, 'warning')
      return redirect(url_for(redirect_url))
    return False
      

