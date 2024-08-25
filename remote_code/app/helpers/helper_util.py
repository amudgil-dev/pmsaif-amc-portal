from datetime import date, timedelta
import random
from flask_login import current_user
from flask_mail import Mail, Message
import os , ssl ,smtplib
from flask import Flask, render_template, url_for,send_file,session,redirect,jsonify,flash,current_app

# from app import app
from email.message import EmailMessage
from flask import request
# from barcode import generate
# from barcode.writer import ImageWriter
from io import BytesIO
import threading

# from modules.db_schema import PMSMaster, UserRole

# from modules.route_users import ResetRequestForm
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
# from extensions import mail


# current_app.config['MAIL_SERVER']='smtp.gmail.com'
# current_app.config['MAIL_PORT'] = 465
# current_app.config['MAIL_USERNAME'] = 'dmudgilfun@gmail.com' 
# current_app.config['MAIL_PASSWORD'] = 'nzfv kjce umlt nmsz'
# current_app.config['MAIL_USE_TLS'] = False
# current_app.config['MAIL_USE_SSL'] = True
# mail = Mail(current_app)


from app.models.models import  PMSMaster, PMSMaster, UserRole
from app.extensions import db,mail

def email_resetlink(reset_link, receiver_email):
    print('in email_resetlink()')
    print(reset_link)
    print(receiver_email)
    print(len(receiver_email))    
    subject = 'reset your password for PMSAIFWorld AMC Portal'
    msg = Message('Password Reset Request!', sender='noreply@demo.com', recipients=[receiver_email])
    msg.body = f''' 

            To reset your password, please follow the link below

            {reset_link}
          
             This is valid for next 5 minutes"

            If you didn't send a password reset request, please ignore this email.

        '''
    print(f" msg = {msg}")
    mail.send(msg)

def email_activationlink(activation_link, receiver_email):
    print('in email_resetlink()')
    print(activation_link)
    # print(receiver_email)
    # print(len(receiver_email))    
    subject = 'reset your password for Eventbyte'
    msg = Message('Account Activation Request!', sender='noreply@demo.com', recipients=[receiver_email])
    msg.body = f''' 

            Welcome to PMSAIF World!
            
            To activate your account and submit monthly performance of PMS, please click the link below

            {activation_link}
          
             This is valid for next 5 minutes"

            If you didn't create account with EventByte, please ignore this email.

        '''

    mail.send(msg)


def generate_resetlink(user):
    print('generate_resetlink()...')
    token = user.get_token()
    reset_link = url_for('auth.reset_password', token=token, _external=True)

    return reset_link

def generate_activationlink(user):
    print('generate_activationlink()...')
    token = user.get_token()
    reset_link = url_for('auth.activate_account', token=token, _external=True)

    return reset_link


# def generate_barcode(data):

#     buffer = BytesIO()
#     generate('code128', data, writer=ImageWriter(), output=buffer)
#     buffer.seek(0)

#     response = send_file(buffer, mimetype='image/png')
#     return response


# User helper

def set_user_in_session(session, user):
    print('set session()')
    # print(str(user.id)+ ' is set in session')
    # session['session_user_id'] = user.id
    # session['session_user_role'] = user.userrole_id
    session.permanent = False
    session['USER_NAME'] = user.fname + ' ' + user.lname
    session['USER_ID'] = user.id
    session['IS_AUTHENTICATED'] = True
    session['USER_ROLE'] = user.userrole_id
    pms_list = getPmsIdsForUser(user)
    print(pms_list)
    
    session['PMS_LIST'] = pms_list
    print("Session is set")
    
    
    # print(pms_list)
    

def getPmsIdsForUser(user):
    # print('getPmsIdsForUser()')
    
    pms_ids = db.session.query(PMSMaster.pms_id).filter_by(amc_id=user.amc_id).all()


    # Extract the pms_id from the query result
    return [pms_id[0] for pms_id in pms_ids]

def get_user_details_in_session(session):
    # print(str(user.id)+ ' is set in session')
    # session['session_user_id'] = user.id
    # session['session_user_role'] = user.userrole_id
    
        
    user_id = session.get('USER_ID', None)
    user_name = session.get('USER_NAME', None)
    user_role = session.get('USER_ROLE', None)
    auth_status = session.get('IS_AUTHENTICATED', None)
    pms_list = session.get('PMS_LIST', None)
    
        # user_id = session['USER_ID']
        # user_name = session['USER_NAME']
        # user_role = session['USER_ROLE']
        # auth_status = session['IS_AUTHENTICATED']
        # pms_list = session['PMS_LIST']
        

    return user_id, user_name, user_role, auth_status, pms_list

def checkAuthZ(user_id,pms_id):
    print(f"checkAuthZ( {user_id, pms_id} ) ")     
    
    pms_id = int(pms_id)
    
    result = False
    # print(str(user.id)+ ' is set in session')
    # session['session_user_id'] = user.id
    # session['session_user_role'] = user.userrole_id
    
    try:
        user_id = session['USER_ID']
        user_name = session['USER_NAME']
        user_role = session['USER_ROLE']
        auth_status = session['IS_AUTHENTICATED']
        pms_list = session['PMS_LIST']
        
        if auth_status is False or user_id is None:
            print(f" auth_status = {auth_status} and user_id = {user_id}")
            return result
        
   
               
        submitter_role_id = UserRole.query.filter_by(name="SUBMITTER").first().id
        print(f" user_role = {user_role} and  submitter_role_id = {submitter_role_id} and pms_id = {pms_id} pms_list = {pms_list} ")
        
        print(f"pms_id type: {type(pms_id)}, pms_list types: {[type(i) for i in pms_list]}")       
        
        print('checked types     *******************') 
                
        if user_role == submitter_role_id:
            print('role ids matched')
            if pms_id in pms_list:
                print(' PMS ID Found in list ...')
                result = True
            else:
                print('pms_id not found...')
        else:
            print(f"Roles are not matching user_role ={user_role} and submitter_role_id = {submitter_role_id} and type of role = {type(user_role)} and type of sub type = {type(submitter_role_id)}   ")
            
    except:
        print(' Exception in checking authorisation')
    
    print(f" final result = {result}")
    return result
        
def enforceAuthz(user_id,pms_id):
    print(f"enforceAuthz( {pms_id} ) ") 
    authz = checkAuthZ(user_id,pms_id)
    if not authz:
        print('You are not authorised to access the PMS you requested, please contat PMSAIF Administrator')
        flash('You are not authorised to access the PMS you requested, please contat PMSAIF Administrator or login with other account!', 'danger')
        return False
    
    return True
    
  # If AuthZ are correct then proceed...    

def get_user_in_session(session):

    try:
        user_id = session['USER_ID']
    except KeyError:
        user_id = None

    return user_id


def get_user_role_in_session(session):

    try:
        user_id = session['USER_ID']
        userrole_id = session['USER_ROLE']
    except KeyError:
        user_id = None
        userrole_id = None

    # print(str(user_id)+ '  and '+ str(userrole_id) +' pulled from session')
    return user_id, userrole_id

def pop_user_in_session(session):

    user_id = session.pop('USER_ID',None)
    session.pop('USER_ROLE',None)
    session.pop('USER_NAME',None)
    session.pop('IS_AUTHENTICATED',None)
    session.pop('PMS_LIST',None)    
    # print(str(user_id)+ '  and '+ str(userrole_id) +' popped from session')
    return user_id


def isAdmin(session):
    
    try: 
        user_id, user_role = get_user_role_in_session(session)
        admin_role_id = UserRole.query.filter_by(name="ADMIN").first().id
        if user_role == admin_role_id:
            return True, user_id, user_role
        else:
            return False , user_id, user_role
    except:
        return False

# def getPmsIdForUser(user):
    
    
#     pms_list = PMSMster.query.filter_by(name="ADMIN").first().id
#     if user_role == admin_role_id:
#         return True, user_id, user_role
#     else:
#         return False , user_id, user_role
    
def getLastMonthYYMM():
  today = date.today()  
  first = today.replace(day=1)
#   print(first)
  last_month = first - timedelta(days=1)
#   print(last_month)
  year = last_month.strftime("%Y")
  prev_month = last_month.strftime("%m")
  return year, prev_month


# Function to generate single number or range with dash
def generate_range(row):
    if row['stocks_min'] == row['stocks_max']:
        return str(row['stocks_min'])
    else:
        return str(row['stocks_min']) + '-' + str(row['stocks_max'])


def get_missing_months(existing_data):
    # Convert existing data to datetime objects
    existing_dates = [date(year, month, 1) for year, month in existing_data]

    # Find the earliest and latest dates
    earliest_date = min(existing_dates)
    latest_date = max(existing_dates)

    # Get the previous month from today
    today = date.today()
    previous_month = today.replace(day=1) - relativedelta(days=1)

    # If the latest date is more recent than the previous month, use the previous month
    end_date = max(latest_date, previous_month)

    # Generate all months from earliest to end date
    all_months = []
    current = earliest_date
    while current <= end_date:
        all_months.append(current)
        current += relativedelta(months=1)

    # Find missing months
    missing_months = [d for d in all_months if d not in existing_dates]

    # Convert missing months to (year, month) format
    return [(d.year, d.month) for d in missing_months]