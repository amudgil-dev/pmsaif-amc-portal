from sqlite3 import IntegrityError
from sqlalchemy.exc import SQLAlchemyError
from flask import Blueprint, get_flashed_messages, render_template, request,flash,redirect, url_for,jsonify
from flask_login import login_required, current_user
from app.helpers.helper_util import enforceAuthz, getLastMonthYYMM, isAdmin
from app.helpers.queries import getPmsListing, getPmsDashDataList, getPmsSectors
from app.models.models import AMCMaster, PMSMaster, PMSPerformance, PMSSector, SectorMaster, Transaction
from app.extensions import db
from app.forms.forms import AddTransactionForm, PMSMasterEditForm, PMSPerformanceEditForm, PMSPerformanceForm
from app.helpers.auth_helper import AuthHelper
from datetime import date, datetime, timedelta
from app.helpers.helper_transaction import safe_transaction

bp_sectors = Blueprint('sectors', __name__)


@bp_sectors.route('/pmssectors/<int:pms_id>', methods=['GET'])
@bp_sectors.route('/admin/pmssectors/<int:pms_id>', methods=['GET'])
@login_required
@AuthHelper.check_session
@AuthHelper.check_pms_authorisations
def sector_holding(pms_id):
    print("sector_holding()")

    get_flashed_messages() # Clear Flash Message    
    form = SectorSearchForm()

    pms_sectors = getPmsSectors(pms_id)
    pms = PMSMaster.query.filter_by(pms_id=pms_id).first()
    return render_template('form_edit_sector_holdings.html', 
                            is_authenticated = current_user.is_authenticated,
                            is_admin=isAdmin(current_user.userrole_id),      
                            user_name= current_user.fname + " " + current_user.lname,                           
                           form=form,
                           pms_sectors=pms_sectors,
                           page_heading="sector Holdings for "+pms.name,
                           pms=pms
                           )

from app.forms.forms import SectorSearchForm



@bp_sectors.route('/autocompsector', methods=['GET'])
@login_required
@AuthHelper.check_session
@AuthHelper.check_pms_authorisations
def autocomplete_sector():
    # print('autocomplete_sector')
    # Simulate fetching relevant data based on the user's input

    query = request.args.get('query', '')

    # result  = getDataFromList(query)
    result = findMatchingSectors(query)

    # print(result)

    return jsonify(result)


def getDataFromList(query):
    # Filter data based on the user's input (first three characters)
        # Replace this with your actual data fetching logic from the database or external API
    sector_data = ['sector1', 'sector2','sector21','sector211','sector2111', 'sector3', 'ISIN1', 'ISIN2', 'SYMBOL1', 'SYMBOL2']

    result = [item for item in sector_data if item.lower().startswith(query.lower())]
    return result


def findMatchingSectors(query):
    print('findMatchingSectors()')
     # Query the database for sectors matching the user's input
    matching_sectors = SectorMaster.query.filter(
        (SectorMaster.name.ilike(f'{query}%')) |
        (SectorMaster.sector_code.ilike(f'{query}%'))
    ).all()

    # print(matching_sectors)

    # Extract relevant information from matching sectors
    result = []
    
    for sector in matching_sectors:
        # dict = {'label': sector.name, 'value': sector.id, 'name': sector.name, 'code': sector.sector_code}
        dict = {'label': sector.name, 'value': sector.id, 'name': sector.name, 'stock_symbol': sector.sector_code, 'isin': sector.sector_code}
        result.append(dict)
    
    return result


@bp_sectors.route('/selectedsectors', methods=['POST'])
@bp_sectors.route('/admin/selectedsectors', methods=['POST'])
@login_required
@AuthHelper.check_session
@AuthHelper.check_pms_authorisations
def selected_sectors():
    print('selected_sectors()')
    print('POST')

    try:
        print(' before getting request ')
        data = request.get_json()
        print(f" after getting request - data = {data}")

        # print(data)
        # print(type(data))
        # print("PMS ID saving holdings @@@@@@@@@@ -->", data['pmsId'])
        pms_id = data['pms_id']
        
        print(f"selected_sectors() = {pms_id}")
        
        # if not enforceAuthz(pms_id):
        #     print('AuthZ Failed and redirecting')
        #     return redirect(url_for('pmslist'))        

        # if 'selectedsectorIds' not in data:
        #     return jsonify({'error': 'Invalid request data'}), 400

        get_flashed_messages() # Clear flash messages
        selected_sectors = data['selectedSectorData']
        # print(type(selected_sectors))

        # print(' -- before upsert sectors ---')

        upsertPmsSectors(pms_id, selected_sectors)
        
        # print(' -- after upsert sectors ---')
 
        return "inserted"

    except Exception as e:
        print(' -- error in selected_sectors ---')
        print(e)
        return jsonify({'error': str(e)}), 500

def upsertPmsSectors(pms_id, selected_sectors):
    print(f'Upserting sectors for PMS ID: {pms_id}')
    get_flashed_messages()  # Clear flash messages

    try:
        with safe_transaction():
            # Delete existing sectors
            deleted = PMSSector.query.filter_by(pms_id=pms_id).delete()
            print(f"Deleted {deleted} existing sectors for PMS ID {pms_id}")

            # Prepare and insert new sectors
            sectors_to_store = []
            for sector in selected_sectors:
                db_sector = SectorMaster.query.get(sector['sectorId'])
                if db_sector:
                    sectors_to_store.append(
                        PMSSector(
                            pms_id=pms_id,
                            sector_id=db_sector.id,
                            pct_deployed=sector['quantity'],
                            created_at=datetime.utcnow()
                        )
                    )
                else:
                    print(f"Warning: Sector with ID {sector['sectorId']} not found in the database")

            # Bulk insert new sectors
            db.session.bulk_save_objects(sectors_to_store)
            print(f"Inserted {len(sectors_to_store)} new sectors for PMS ID {pms_id}")

        print(f"Successfully upserted sectors for PMS ID {pms_id}")
        return True, f"Successfully updated {len(sectors_to_store)} sectors for PMS ID {pms_id}"

    except SQLAlchemyError as e:
        error_msg = f"Database error in upsertPmsSectors: {str(e)}"
        print(error_msg)
        return False, error_msg
    except Exception as e:
        error_msg = f"Error in upsertPmsSectors: {str(e)}"
        print(error_msg)
        return False, error_msg