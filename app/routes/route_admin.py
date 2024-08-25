import calendar
from datetime import datetime
from sqlite3 import IntegrityError
from flask import Blueprint, render_template, redirect, send_file, url_for, flash,current_app,request
from flask_login import login_user, logout_user, login_required, current_user
from app.helpers.helper_excel import write_Excel_report
from app.helpers.helper_util import generate_resetlink,email_resetlink, getLastMonthYYMM
from app.helpers.queries import getIndexListing, getIndexPerformance, getPerformanceReport
from app.models.models import IndexMaster, IndexPerformance, User
from app.forms.forms import DummyForm, IndexPerformanceEditForm, IndexPerformanceForm, ResetPasswordForm, ResetRequestForm, SigninForm
from app.helpers.auth_helper import AuthHelper
from app.helpers.logging_helper import debug, info, warning, error, critical, log_exception, log_function_call
from app.extensions import login_manager, db

bp_admin = Blueprint('admin', __name__)


@bp_admin.route('/admin')
@login_required
@AuthHelper.check_session
@AuthHelper.check_admin_authorisations
def admin_home():
  # print('admin_home()')

  # user_id, user_name, user_role, auth_status, pms_list = get_user_details_in_session(session)
    
  return render_template('admin_home.html',
                         is_authenticated = current_user.is_authenticated,
                         user_name= current_user.fname + " " + current_user.lname,
                         )


@bp_admin.route('/indexlist')
@login_required
@AuthHelper.check_session
def index_list():
  # print('index_list()')
  # loggedin = 0
  # user_name = ""

  # user_id, user_name, user_role, auth_status,pms_list = get_user_details_in_session(session)

  # if isAdmin(session) == False:
  #    flash('You are not authorised to view this page, please contact Administrator!', 'danger' )
  #    return redirect(url_for('users.logout'))

  # loggedin = 1

      
  index_list = getIndexListing()
  
  # booking_id = db.session.query(Booking).filter(and_(Booking.event_id==event_id, Booking.user_id == uid  )).order_by(Booking.id.desc()).first().id
  
  return render_template('admin_index_listing.html',
                         is_authenticated = current_user.is_authenticated,
                         user_name= current_user.fname + " " + current_user.lname,
                         page_heading="List of Index",
                         index_list=index_list)


@bp_admin.route('/viewindexperf/<int:index_id>')
@login_required
@AuthHelper.check_session
def view_indexperf(index_id):
  print('view_indexperf()')
  # loggedin = 0
  # user_name = ""

  # user_id, user_name, user_role, auth_status,pms_list = get_user_details_in_session(session)

  # if isAdmin(session) == False:
  #    flash('You are not authorised to view this page, please contact Administrator!', 'danger' )
  #    return redirect(url_for('users.logout'))

  # loggedin = 1

      
  index_perf = getIndexPerformance(index_id)

  return render_template('admin_index_perf.html',
                         is_authenticated = current_user.is_authenticated,
                         user_name= current_user.fname + " " + current_user.lname,
                         page_heading="Index Performance - History",
                         index_perf=index_perf)




@bp_admin.route('/editindexperf/<int:index_id>', methods=['GET', 'POST'])
@login_required
@AuthHelper.check_session
def edit_indexperf(index_id):
  # print('in edit_indexperf()')

  # print("index_id ==>", index_id)
  
  # user_id, user_name, user_role, auth_status,pms_list = get_user_details_in_session(session)
  # if isAdmin(session) == False:
  #    flash('You are not authorised to view this page, please contact Administrator!', 'danger' )
  #    return redirect(url_for('users.logout'))

  # loggedin = 1


  index_perf = IndexPerformance.query.filter_by(id=index_id).order_by(IndexPerformance.id.desc()).first()

  if index_perf is None:
    flash('Not Authorised, please contat PMSAIF Administrator!', 'danger')
    # print('Index Id not found not valid')
    return redirect(url_for('admin.admin_home'))
  
  index = IndexMaster.query.filter_by(id=index_perf.index_id).first()


  # print(index_perf.p_month)
  # print(index_perf)
  form = IndexPerformanceEditForm(obj=index_perf)
  # print(' ------- perf is out -----')
  
  if request.method == 'GET':
      return render_template('admin_form_edit_index_performance.html', 
                                is_authenticated = current_user.is_authenticated,
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
def new_indexperf(index_id):
  # print('in new_indexperf()')

  # # print("index_id ==>", index_id)
  # user_id, user_name, user_role, auth_status,pms_list = get_user_details_in_session(session)
  # if isAdmin(session) == False:
  #    flash('You are not authorised to view this page, please contact Administrator!', 'danger' )
  #    return redirect(url_for('users.logout'))

  # loggedin = 1


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
        return redirect(url_for('admin.admin_home'))
        # Process the data as needed (e.g., store in a database)


@bp_admin.route('/pmsreports', methods=['GET', 'POST'])
@login_required
@AuthHelper.check_session
def pms_reports():
  # print('in pms_reports()')
  form = DummyForm()
  # if isAdmin(session) == False:
  #    flash('You are not authorised to view this page, please contact Administrator!', 'danger' )
  #    return redirect(url_for('users.logout'))

  # user_id, user_name, user_role, auth_status, pms_list = get_user_details_in_session(session)
  
  # loggedin = 1

  if request.method == 'POST':
    # print('in post')


    selected_month_year = request.form['monthYear']
    selected_month = int(selected_month_year[:2])  # Extract month as integer
    selected_year = int(selected_month_year[2:])   # Extract year as integer

    # print(selected_month, selected_year)
  
    month = selected_month
    year = selected_year
    df = getPerformanceReport(month, year)

    df = df.fillna('-')
    # df = df.replace(np.nan, '---')

    # print(df['Large'])
    
    # constraining the relevant columns to two decimal place only
    df.Large = df.Large.round(2)
    df.Mid = df.Mid.round(2)
    df.Small = df.Small.round(2)    
    df.cash = df.cash.round(2)    
    # df['Large'] = df['Large'].map('{:,.2f}'.format)
    # df['Mid'] = df['Mid'].map('{:,.2f}'.format)
    # df['Small'] = df['Small'].map('{:,.2f}'.format)
    # df['Cash'] = df['Cash'].map('{:,.2f}'.format)    

    keys = df.keys()

    # print(keys)
    # print(len(keys))
    lists= df.values.tolist()
    
    # print(lists)
    
    temp_date  = datetime(int(year), int(month), 1)
    date_display = temp_date.strftime("%B, %Y")
 
    return render_template('admin_pms_report.html', 
                                  is_authenticated = current_user.is_authenticated,
                                  user_name= current_user.fname + " " + current_user.lname,
                                  month=month,
                                  year= year,
                                  form=form,
                                  page_heading="All PMS Report  for  - " +date_display,   
                          keys=keys,lists=lists)

  if request.method == 'GET':
    # print('in get')
    return render_template('admin_pms_report.html', 
                                is_authenticated = current_user.is_authenticated,
                                user_name= current_user.fname + " " + current_user.lname,
                                form=form,
                                page_heading=" PMS Report  " 
                        )


@bp_admin.route('/download_excel', methods=['GET','POST'])
@login_required
@AuthHelper.check_session
def download_excel():
    # print('in download_excel()')
    form = DummyForm()
    
    # selected_month_year = request.form['month']
    # selected_month = int(selected_month_year[:2])  # Extract month as integer
    # selected_year = int(selected_month_year[2:])   # Extract year as integer

    month = request.form.get('month')  # Get the selected month from the form data  
    year = request.form.get('year')
    month = int(month)
    year = int(year)
    # Get the month name from its number
    month_name = calendar.month_name[month]

    # Format the string
    formatted_string = f"{year}_{month_name[:3]}"

    file_name ="PMSReport_"+ formatted_string+".xlsx"
    df = getPerformanceReport(month, year)
    # df = df.fillna('-')
    excel_file = write_Excel_report(df)
    print('download_excel() ')

    # Return the Excel file as an attachment
    return send_file(excel_file, download_name=file_name, as_attachment=True)



# @bp.route('/loadamc', methods=['GET'])
# def check_loac_amc():
#     load_amc()

#     return "AMC Loaded"

# @bp.route('/loadpms', methods=['GET'])
# def check_loac_pms():
#     load_pms()

#     return "AMC Loaded"

