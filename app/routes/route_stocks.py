from sqlite3 import IntegrityError
from sqlalchemy.exc import SQLAlchemyError
from flask import Blueprint, get_flashed_messages, render_template, request,flash,redirect, url_for,jsonify
from flask_login import login_required, current_user
from app.helpers.helper_transaction import safe_transaction
from app.helpers.helper_util import enforceAuthz, getLastMonthYYMM, isAdmin
from app.helpers.queries import getPmsListing, getPmsDashDataList, getPmsStocks
from app.models.models import AMCMaster, PMSMaster, PMSPerformance, PMSStock, StockMaster, Transaction
from app.extensions import db
from app.forms.forms import AddTransactionForm, PMSMasterEditForm, PMSPerformanceEditForm, PMSPerformanceForm
from app.helpers.auth_helper import AuthHelper
from datetime import date, datetime, timedelta

bp_stocks = Blueprint('stocks', __name__)


@bp_stocks.route('/pmsstocks/<int:pms_id>', methods=['GET'])
@bp_stocks.route('/admin/pmsstocks/<int:pms_id>', methods=['GET'])
@login_required
@AuthHelper.check_session
@AuthHelper.check_pms_authorisations
def stock_holding(pms_id):
    print("stock_holding()")
    # print(' PMSID ==> view holding £££££££££££££ ==>', pms_id)

    get_flashed_messages() # Clear flash messages
            
    # print('search4')
    form = StockSearchForm()

    pms_stocks = getPmsStocks(pms_id)
    pms = PMSMaster.query.filter_by(pms_id=pms_id).first()
    return render_template('form_edit_stock_holdings.html', 
                         is_authenticated = current_user.is_authenticated,
                         is_admin=isAdmin(current_user.userrole_id),                               
                         user_name= current_user.fname + " " + current_user.lname,                           
                           form=form,
                           pms_stocks=pms_stocks,
                           page_heading="Stock Holdings for "+pms.name,
                           pms=pms
                           )

from app.forms.forms import StockSearchForm


@bp_stocks.route('/autocompstock', methods=['GET'])
@bp_stocks.route('/admin/autocompstock', methods=['GET'])
@login_required
@AuthHelper.check_session
@AuthHelper.check_pms_authorisations
def autocomplete_stocks():
    # print('autocomplete_stocks()')
    # Simulate fetching relevant data based on the user's input

    query = request.args.get('query', '')

    # result  = getDataFromList(query)
    result = findMatchingStocks(query)

    # print(result)

    return jsonify(result)


def getDataFromList(query):
    # Filter data based on the user's input (first three characters)
        # Replace this with your actual data fetching logic from the database or external API
    stock_data = ['Stock1', 'Stock2','Stock21','Stock211','Stock2111', 'Stock3', 'ISIN1', 'ISIN2', 'SYMBOL1', 'SYMBOL2']

    result = [item for item in stock_data if item.lower().startswith(query.lower())]
    return result


def findMatchingStocks(query):
    print('findMatchingStocks')
     # Query the database for stocks matching the user's input
    matching_stocks = StockMaster.query.filter(
        (StockMaster.name.ilike(f'{query}%')) |
        (StockMaster.stock_symbol.ilike(f'{query}%')) |
        (StockMaster.isin_code.ilike(f'{query}%'))
    ).all()

    # print(matching_stocks)

    # Extract relevant information from matching stocks
    result = []
    
    for stock in matching_stocks:
        dict = {'label': stock.name, 'value': stock.id, 'name': stock.name, 'stock_symbol': stock.stock_symbol, 'isin': stock.isin_code}
        result.append(dict)
    
    return result


@bp_stocks.route('/selectedstocks', methods=['POST'])
@login_required
@AuthHelper.check_session
@AuthHelper.check_pms_authorisations
def selected_stocks():
    print('selected_stocks')

    try:
        data = request.get_json()

        print(data)
        # print(type(data))
        # print("PMS ID saving holdings @@@@@@@@@@ -->", data['pmsId'])
        print(' I AM DOWN here ..')
        pms_id = data['pms_id']
         
        print(' I WANT TO SEE YOU pms_id')
        get_flashed_messages() # Clear flash messages
        

        # if 'selectedStockIds' not in data:
        #     return jsonify({'error': 'Invalid request data'}), 400
        print(' I WANT TO SEE YOU')
        selected_stocks = data['selectedStockData']
        print(' I CAN SEE YOU')
        
        print(selected_stocks)

        print('upserting stocks')
        upsertPmsStocks(pms_id, selected_stocks)
 
        return "inserted"

    except Exception as e:
        print(e)
        return jsonify({'error': str(e)}), 500



def upsertPmsStocks(pms_id, selected_stocks):
    print(f'Upserting stocks for PMS ID: {pms_id}')
    get_flashed_messages()  # Clear flash messages

    try:
        with safe_transaction():
            # Delete existing sectors
            deleted = PMSStock.query.filter_by(pms_id=pms_id).delete()
            print(f"Deleted {deleted} existing stocks for PMS ID {pms_id}")

            # Prepare and insert new stocks
            
            print(f"selected_stocks = {selected_stocks} ")
            stocks_to_store = []
            for stock in selected_stocks:
                db_stock = StockMaster.query.get(stock['stockId'])
                if db_stock:
                    stocks_to_store.append(
                        PMSStock(
                            pms_id=pms_id,
                            stock_id=db_stock.id,
                            pct_deployed=stock['quantity'],
                            created_at=datetime.utcnow()
                        )
                    )
                else:
                    print(f"Warning: Stock with ID {stock['stockId']} not found in the database")

            print(' storing bulk ')
            # Bulk insert new sectors
            db.session.bulk_save_objects(stocks_to_store)
            print(f"Inserted {len(stocks_to_store)} new stocks for PMS ID {pms_id}")

        print(f"Successfully upserted sectors for PMS ID {pms_id}")
        return True, f"Successfully updated {len(stocks_to_store)} stocks for PMS ID {pms_id}"

    except SQLAlchemyError as e:
        error_msg = f"Database error in upsertPmsStocks: {str(e)}"
        print(error_msg)
        return False, error_msg
    except Exception as e:
        error_msg = f"Error in upsertPmsStocks: {str(e)}"
        print(error_msg)
        return False, error_msg