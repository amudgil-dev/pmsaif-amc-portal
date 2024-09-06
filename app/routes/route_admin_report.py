import calendar
from datetime import datetime
from sqlite3 import IntegrityError
from flask import Blueprint, render_template, redirect, send_file, url_for, flash,current_app,request
from flask_login import login_user, logout_user, login_required, current_user
from markupsafe import Markup
from app.helpers.helper_excel import write_PmsPerf_Excel_report, write_most_recent_nav_excel_report
from app.helpers.helper_util import generate_resetlink,email_resetlink, getLastMonthYYMM, isAdmin
from app.helpers.queries import getAdminPmsListingByIndex, getIndexListing, getIndexPerformance, getMostRecentNavReport,  getPerformanceReport,getAmcListing,getAdminPmsListing, getUserListing
from app.models.models import AMCMaster, IndexMaster, IndexPerformance, User, UserRole
from app.forms.forms import DummyForm, IndexPerformanceEditForm, IndexPerformanceForm, ResetPasswordForm, ResetRequestForm, SigninForm, SignupForm
from app.helpers.auth_helper import AuthHelper
from app.helpers.logging_helper import debug, info, warning, error, critical, log_exception, log_function_call
from app.extensions import login_manager, db

bp_admin_report = Blueprint('admin_report', __name__)






@bp_admin_report.route('/admin/pmsperfreport', methods=['GET', 'POST'])
@login_required
@AuthHelper.check_session
@AuthHelper.check_admin_authorisations
def pms_perf_report():
  print('in pms_perf_report()')
  form = DummyForm()


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
 
    return render_template('admin_report_pms.html', 
                                  is_authenticated = current_user.is_authenticated,
                                  is_admin=isAdmin(current_user.userrole_id),                                  
                                  user_name= current_user.fname + " " + current_user.lname,
                                  month=month,
                                  year= year,
                                  form=form,
                                  page_heading="All PMS Report  for  - " +date_display,   
                          keys=keys,lists=lists)

  if request.method == 'GET':
    # print('in get')
    return render_template('admin_report_pms.html', 
                                is_authenticated = current_user.is_authenticated,
                                is_admin=isAdmin(current_user.userrole_id),                                
                                user_name= current_user.fname + " " + current_user.lname,
                                form=form,
                                page_heading=" PMS Report  " 
                        )


@bp_admin_report.route('/dloadpmsexcel', methods=['GET','POST'])
@login_required
@AuthHelper.check_session
@AuthHelper.check_admin_authorisations
def dload_pms_perf_excel():
    # print('in dload_pms_perf_excel()')
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

    file_name ="PmsPerformanceReport_"+ formatted_string+".xlsx"
    df = getPerformanceReport(month, year)
    # df = df.fillna('-')
    excel_file = write_PmsPerf_Excel_report(df)
    print('download_excel() ')

    # Return the Excel file as an attachment
    return send_file(excel_file, download_name=file_name, as_attachment=True)


######################## OTHER REPORTS ########################

@bp_admin_report.route('/admin/mrnavreport', methods=['GET'])
@login_required
@AuthHelper.check_session
@AuthHelper.check_admin_authorisations
def most_recent_nav_report():
  print('in most_recent_nav_report()')
  form = DummyForm()


  if request.method == 'GET':
    # print('in post')


    df = getMostRecentNavReport()
    # print(df)

 

    keys = df.keys()

    # print(keys)
    # print(len(keys))
    lists= df.values.tolist()
    
 
    return render_template('admin_report_pms_nav.html', 
                                  is_authenticated = current_user.is_authenticated,
                                  is_admin=isAdmin(current_user.userrole_id),                                  
                                  user_name= current_user.fname + " " + current_user.lname,
                                  # month=month,
                                  # year= year,
                                  form=form,
                                  page_heading="Most Recent NAV - All PMS" ,   
                          keys=keys,lists=lists)


@bp_admin_report.route('/admin_report/dlmrnavreport', methods=['GET','POST'])
@login_required
@AuthHelper.check_session
@AuthHelper.check_admin_authorisations
def dload_most_recent_nav_report():
    print('in dload_most_recent_nav_report()')
    form = DummyForm()
    
    # selected_month_year = request.form['month']
    # selected_month = int(selected_month_year[:2])  # Extract month as integer
    # selected_year = int(selected_month_year[2:])   # Extract year as integer

    # month = request.form.get('month')  # Get the selected month from the form data  
    # year = request.form.get('year')
    
    # print(f" month = {month} and year = {year}")
    # month = int(month)
    # year = int(year)
    # Get the month name from its number
    now = datetime.now()
    
    month_name = calendar.month_name[now.month]

    # Format the string
    formatted_string = f"{now.year}_{month_name[:3]}_{now.day}"

    file_name ="PmsNavReport_"+ formatted_string+".xlsx"
    # df = None
    df = getMostRecentNavReport()
    df = df.drop('amc_id', axis=1)
    # df = df.fillna('-')
    excel_file = write_most_recent_nav_excel_report(df)
    print('download_excel() ')

    # Return the Excel file as an attachment
    return send_file(excel_file, download_name=file_name, as_attachment=True)
