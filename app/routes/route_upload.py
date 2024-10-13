from flask import Blueprint, render_template, request,flash,redirect, url_for
from flask_login import login_required, current_user
from app.helpers.helper_upload_parser import parse_excel
from app.helpers.helper_util import isAdmin
from app.helpers.queries import getPmsDashDataList, getPmsDetails
from app.models.models import Transaction
from app.extensions import db
from app.forms.forms import AddTransactionForm
from app.helpers.auth_helper import AuthHelper
from datetime import datetime

bp_upload = Blueprint('upload', __name__)



@bp_upload.route('/uploadamcperf/<int:pms_id>', methods=['GET', 'POST'])
@bp_upload.route('/admin/uploadamcperf/<int:pms_id>', methods=['GET', 'POST'])
@login_required
@AuthHelper.check_session
@AuthHelper.check_pms_authorisations
def upload_amc_perf(pms_id):
    print('upload_amc_perf()')
    # pms,index_perf,pms_details,pms_stocks, pms_sectors = getPmsDashDataList(pms_id)  


    pms,index_perf,pms_details,pms_stocks, pms_sectors = getUploadedData()

    print('--- BEFORE ROUTE ---')
    print(pms.one_month)
    print(pms.pms_id)
    print('--- JUST BEFORE ROUTE ---')
    

    temp_date  = datetime(pms.year, pms.month, 1)
    date_display = temp_date.strftime("%B, %Y")

    return render_template('pms_dashboard_upload.html',
                            is_authenticated = current_user.is_authenticated,
                            is_admin=isAdmin(current_user.userrole_id),      
                            user_name= current_user.fname + " " + current_user.lname,
                            page_heading="Uploaded Data for confirmation - "+pms.pms_name,
                            pms=pms,
                            date_display=date_display,
                            index=index_perf,
                            pms_details=pms_details,
                            pms_stocks=pms_stocks,
                            pms_sectors=pms_sectors
                            )
  
  
def getUploadedData(pms_id):
    pms = getPmsDetails(pms_id)
    index_perf = None
    pms_details = None
    pms_stocks = None
    pms_sectors = None
    

    book_name = 'tempdata/UIforAMCTemplate1.xlsx'
    
    header_info , strategy_list, amc_data = parse_excel(book_name)
    # print("starting ...")
    # wk = xw.books.open(book_name)
                
    # header_info , strategy_list = readHeader(wk,book_name=book_name)
    # amc_data = readDataFromSheets(wk,book_name=book_name, strategies=strategy_list)

    print(header_info)
    print('*****')
    print(strategy_list)
    print('*****')
    print(amc_data)
        
    return pms,index_perf,pms_details,pms_stocks, pms_sectors