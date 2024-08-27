from sqlite3 import IntegrityError
from app import db
import csv
import os
import numpy as np
import pandas as pd
from datetime import datetime, timezone
from app.models.models import (
    User1, 
    Transaction,
    StructureMaster,
    CategoryMaster,
    AMCMaster,
    IndexMaster,
    StockMaster,
    SectorMaster,
    UserRole,
    User,
    TxnType,
    TxnLog,
    PMSMaster,
    PMSSector,
    PMSStock,
    PMSPerformance,
    IndexPerformance,
    PMSNav,)
import random
from flask import jsonify
from datetime import datetime, timedelta

def create_schema():
        # Create all tables
        db.create_all()
    
def load_sample_data():
    # create_schema()

    # Create sample users
    user1 = User1(username='debit_user', user_type='debit')
    user1.set_password('password')
    user2 = User1(username='credit_user', user_type='credit')
    user2.set_password('password')

    db.session.add_all([user1, user2])
    db.session.commit()

    # Create sample transactions
    for i in range(20):
        txn = Transaction(
            user_id=user1.id if i % 2 == 0 else user2.id,
            txn_date=datetime.utcnow() - timedelta(days=random.randint(0, 30)),
            txn_amount=random.uniform(10, 1000),
            txn_type='debit' if i % 2 == 0 else 'credit'
        )
        db.session.add(txn)

    db.session.commit()
    print("Sample data loaded successfully.")
    


# Get the directory of the current script
current_dir = os.path.dirname(os.path.abspath(__file__))




def load_pms_data():
    print('load_pms_data()')
    try:
        # Create all tables
        # create_schema()
        
        populate_structure_master()
        populate_index_master()
        populate_category_master()
        populate_amc_master()
        populate_pms_master()
        print('*********************** Master Tables (Structure/Index/ Category, amc, pms) Loaded *************************')
        
        loadDummyStock() # used for initialising / boot straping, customers will be able to change it
        loadDummySector() # used for initialising / boot straping, customers will be able to change it
        
        print('*********************** Dummy Stock and Sector Tables Loaded *************************')        
        
        populate_stock_master()   # list of real stocks
        populate_sector_master()  # list of real sectors
        
        print('*********************** Master records for Stock and Sector Tables Loaded *************************')       
                
        # Loading 
        loadUserRole()
        print('*********************** Master records for UserRole Tables Loaded *************************')         
        loadTxnType()
        
        print('*********************** Master records forTxn Type Tables Loaded *************************')      
             
        # creating admin and test users 
        create_test_users() 
        print('*********************** Master records for UserRole and Txn Type Tables Loaded *************************')              
        # Loading the amc users received from businessstore_amc_users
        load_amc_users()
        print('*********************** Master records for UserRole and Txn Type Tables Loaded *************************')              
        
        ### Loading of master data is finished ### 
        # Loading transactional data in the pms and Index tables to bootstrap
        loadDummyPmsSectors()
        print('*********************** dummy records for PMSSectors Loaded *************************')             
        loadDummyPmsStocks()
        print('*********************** dummy records for PMSStocks Loaded *************************')          
        dummy_pmsperf()
        print('*********************** dummy records for PMSPerf Loaded *************************')          
        dummy_indexperf()
        print('*********************** dummy records for Index Loaded *************************')          
        
        
        # Actual NAV Data for all the PMS for last known data, received from Business
        populate_pms_nav()
        print('*********************** dummy records for PMSNav Loaded *************************')          

        

        return (
            jsonify(
                {"message": "Database initialized successfully. All tables created."}
            ),
            200,
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500



# @bp.route("/populate-structure-master", methods=["GET"])
def populate_structure_master():
    try:
        # Drop the existing table and recreate it
        # db.session.execute(text("DROP TABLE IF EXISTS structure_master;"))
        # db.session.commit()
        # db.create_all()
        
        # Construct the path to the CSV file
        FILE_NAME = os.path.join(current_dir, "init_data", "Scheme_id_Benchmark.csv")

        # Read the CSV file
        with open(FILE_NAME, "r") as file:
            csv_reader = csv.DictReader(file)

            # Create a set to store unique structures
            structures = set()

            # Iterate through the CSV and add unique structures to the set
            for row in csv_reader:
                structures.add((int(row["PMS Structure ID"]), row["Structure name"]))


        # print(structures)
        # Populate the StructureMaster table
        
        for structure_id, name in structures:
            structure = StructureMaster(
                structure_id=structure_id,
                name=name,
                created_at=datetime.now(timezone.utc),
            )
            db.session.add(structure)

        # Commit the changes
        db.session.commit()

        return (
            jsonify(
                {
                    "message": f"StructureMaster table populated with {len(structures)} entries."
                }
            ),
            200,
        )
    except Exception as e:
        db.session.rollback()
        print(str(e))
        return jsonify({"error": str(e)}), 500


# @bp.route("/populate-index-master", methods=["GET"])
def populate_index_master():
    try:
        # Drop the existing table and recreate it
        # db.session.execute(text("DROP TABLE IF EXISTS index_master;"))
        # db.session.commit()
        # db.create_all()

        # Construct the path to the CSV file
        FILE_NAME = os.path.join(current_dir, "init_data", "Scheme_id_Benchmark.csv")
        
        # Read the CSV file
        with open(FILE_NAME, "r") as file:
            csv_reader = csv.DictReader(file)

            # Create a set to store unique benchmarks
            benchmarks = set()

            # Iterate through the CSV and add unique benchmarks to the set
            for row in csv_reader:
                benchmarks.add(row["Strategy Benchmark"])

        # Populate the IndexMaster table
        for index, benchmark in enumerate(benchmarks, start=1):
            index_master = IndexMaster(
                index_ref=f"INDEX_{index}",  # Generate a unique index_ref
                name=benchmark,
                index_code=f"CODE_{index}",  # Generate a placeholder index_code
                created_at=datetime.now(timezone.utc),
            )
            db.session.add(index_master)

        # Commit the changes
        db.session.commit()

        return (
            jsonify(
                {
                    "message": f"IndexMaster table populated with {len(benchmarks)} entries."
                }
            ),
            200,
        )
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


# @bp.route("/populate-category-master", methods=["GET"])
def populate_category_master():
    try:
        # Drop the existing table and recreate it
        # db.session.execute(text("DROP TABLE IF EXISTS category_master;"))
        # db.session.commit()
        # db.create_all()
        
        # Construct the path to the CSV file
        FILE_NAME = os.path.join(current_dir, "init_data", "Scheme_id_Benchmark.csv")        

        # Read the CSV file
        with open(FILE_NAME, "r") as file:
            csv_reader = csv.DictReader(file)

            # Create a dictionary to store unique categories
            categories = {}

            # Iterate through the CSV and add unique categories to the dictionary
            for row in csv_reader:
                category_id = int(row["Category ID"])
                category_name = row["Category Name"]
                categories[category_id] = category_name

        # Populate the CategoryMaster table
        for category_id, category_name in categories.items():
            category_master = CategoryMaster(
                category_id=category_id,
                name=category_name,
                created_at=datetime.now(timezone.utc),
            )
            add_returns = db.session.add(category_master)
            print(add_returns)

        # Commit the changes
        db.session.commit()

        return (
            jsonify(
                {
                    "message": f"CategoryMaster table populated with {len(categories)} entries."
                }
            ),
            200,
        )
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


# @bp.route("/populate-amc-master", methods=["GET"])
def populate_amc_master():
    try:

        # Drop the existing table and recreate it
        # db.session.execute(text("DROP TABLE IF EXISTS amc_master;"))
        # db.session.commit()
        # db.create_all()

        # Construct the path to the CSV file
        FILE_NAME = os.path.join(current_dir, "init_data", "Scheme_id_Benchmark.csv")
        
        # Read the CSV file
        with open(FILE_NAME, "r") as file:
            csv_reader = csv.DictReader(file)

            # Create a dictionary to store unique companies
            companies = {}

            # Iterate through the CSV and add unique companies to the dictionary
            for row in csv_reader:
                company_id = int(row["Company ID"])
                company_name = row["Company Name"]
                companies[company_id] = company_name

        # Populate the AMCMaster table
        for amc_id, name in companies.items():
            # print(amc_id, name)
            amc_master = AMCMaster(
                amc_id=amc_id, name=name, created_at=datetime.now(timezone.utc)
            )
            add_return = db.session.add(amc_master)
            # print(add_return)

        # Commit the changes
        db.session.commit()

        return (
            jsonify(
                {"message": f"AMCMaster table populated with {len(companies)} entries."}
            ),
            200,
        )
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


# @bp.route("/populate-pms-master", methods=["GET"])
def populate_pms_master():
    try:
        # print("PMSMaster attributes:", PMSMaster.__table__.columns.keys())

        # Check if the referenced tables are populated
        if (
            AMCMaster.query.count() == 0
            or CategoryMaster.query.count() == 0
            or StructureMaster.query.count() == 0
            or IndexMaster.query.count() == 0
        ):
            return (
                jsonify(
                    {
                        "error": "Please populate AMCMaster, CategoryMaster, StructureMaster, and IndexMaster tables first."
                    }
                ),
                400,
            )

        # Drop the existing table and recreate it
        # db.session.execute(text("DROP TABLE IF EXISTS pms_master;"))
        # db.session.commit()
        # db.create_all()

        index_mapping = {index.name: index.id for index in IndexMaster.query.all()}

        # Construct the path to the CSV file
        FILE_NAME = os.path.join(current_dir, "init_data", "Scheme_id_Benchmark.csv")
        
        # Read the CSV file
        with open(FILE_NAME, "r") as file:
            csv_reader = csv.DictReader(file)

            for row in csv_reader:
                pms_master = PMSMaster(
                    pms_id=int(row["scheme ID"]),
                    amc_id=(int(row["Company ID"])),
                    category_id=(int(row["Category ID"])),
                    structure_id=(int(row["PMS Structure ID"])),
                    name=row["Scheme Name"],
                    index_id=index_mapping.get(row["Strategy Benchmark"]),
                    aum=0.0,  # Default value, update if available in CSV
                    stocks_min=0,  # Default value, update if available in CSV
                    stocks_max=0,  # Default value, update if available in CSV
                    portfolio_pe=0.0,  # Default value, update if available in CSV
                    large_cap=0.0,  # Default value, update if available in CSV
                    mid_cap=0.0,  # Default value, update if available in CSV
                    small_cap=0.0,  # Default value, update if available in CSV
                    cash=0.0,  # Default value, update if available in CSV
                    created_at=datetime.now(timezone.utc),
                )
                # print("hello")
                # print(type(pms_master))

                db.session.add(pms_master)

        # Commit the changes
        db.session.commit()

        return jsonify({"message": "PMSMaster table populated successfully."}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500



# @bp.route("/populate-stock-master", methods=["GET"])
def populate_stock_master():
    try:
        # # Drop the existing table and recreate it
        # db.session.execute(text("DROP TABLE IF EXISTS stock_master;"))
        # db.session.commit()
        # db.create_all()

        # Construct the path to the CSV file
        FILE_NAME = os.path.join(current_dir, "init_data", "EQUITY_L.csv")
        
        msg , stockcount =  load_stocks(FILE_NAME)
        
        

        return (
            jsonify(
                {
                    "message": f"StockMaster table populated with {stockcount} entries."
                }
            ),
            200,
        )
    except Exception as e:
        db.session.rollback()
        print(str(e))
        return jsonify({"error": str(e)}), 500
    

# @bp.route("/populate-sector-master", methods=["GET"])
def populate_sector_master():
    try:
        # Drop the existing table and recreate it
        # db.session.execute(text("DROP TABLE IF EXISTS sector_master;"))
        # db.session.commit()
        # db.create_all()

        # Construct the path to the CSV file
        FILE_NAME = os.path.join(current_dir, "init_data", "scheme_sectors.csv")
        

        msg , sectorcount =  load_sectors(FILE_NAME)
        
        

        return (
            jsonify(
                {
                    "message": f"SectorMaster table populated with {sectorcount} entries."
                }
            ),
            200,
        )
    except Exception as e:
        db.session.rollback()
        print(str(e))
        return jsonify({"error": str(e)}), 500




def loadTxnType():
    txntype_list = [
        TxnType("REGISTER", datetime.now()),
        TxnType("REGISTER_FAILURE", datetime.now()),
        TxnType("LOGIN", datetime.now()),
        TxnType("LOGIN_FAILURE", datetime.now()),
        TxnType("LOGOUT", datetime.now()),
        TxnType("PASSWORD_RESET", datetime.now()),
        TxnType("ACT_ACTIVATION_SUCCESS", datetime.now()),
        TxnType("ACT_ACTIVATION_FAILED", datetime.now()),
        TxnType("FORM_FAILURE", datetime.now()),
        TxnType("EMAIL_NOTIFICATION", datetime.now()),
        TxnType("PERF_ADDED", datetime.now()),
        TxnType("PERF_UPDATED", datetime.now()),
        TxnType("SECTORS_UPDATED", datetime.now()),
        TxnType("STOCKS_UPDATED", datetime.now()),
        TxnType("REPORT_CREATED", datetime.now()),
        TxnType("UNKNOWN", datetime.now()),
    ]
    db.session.add_all(txntype_list)
    db.session.commit()
    # print("Loaded TxnTypes")
    # print("_______________________")



    

def loadUserRole():
    print("loadUserRole()")    
    userrole_list = [
        UserRole("ADMIN", datetime.now()),
        UserRole("SUBMITTER", datetime.now()),
    ]
    db.session.add_all(userrole_list)
    db.session.commit()
    # print("Loaded Roles")
    # print("_______________________")



def load_stocks(FILE_NAME):
    print("load_stocks()")

    # Read the CSV file into a DataFrame
    df = pd.read_csv(FILE_NAME)

    # Display the DataFrame
    # print(df.shape)
    df.columns = df.columns.str.strip().str.upper()
    # print(df.keys())

    df = df[df["SERIES"] != "BE"]

    # print(df.shape)

    df.pop("SERIES")
    df.pop("PAID UP VALUE")
    df.pop("MARKET LOT")
    df.pop("FACE VALUE")
    df.pop("DATE OF LISTING")
    # print(df.shape)

    # popped = df.pop('Scheme Name')
    # df.insert(1, 'Scheme Name', popped)

    df.insert(0, "stock_ref", 1)

    # Add a new column 'CREATED_AT' with current timestamp
    df["created_at"] = datetime.now()

    # print(df.keys())

    df = df.rename(
        columns={
            "SYMBOL": "stock_symbol",
            "NAME OF COMPANY": "name",
            "ISIN NUMBER": "isin_code",
        }
    )

    popped = df.pop("stock_symbol")
    df.insert(2, "stock_symbol", popped)

    # print(df.keys())
    # print(df)

    # Get the underlying database engine
    engine = db.engine
    conn = engine.raw_connection()
    cursor = conn.cursor()

    # Load the DataFrame into the stock_master table
    df.to_sql("stock_master", conn, if_exists="append", index=False)

    # Commit the transaction and close the connection
    conn.commit()
    conn.close()

    return "loaded "+ len(df[0]) + " records" ,  len(df[0])


def load_sectors(FILENAME):
    print("load_sectors()")

    # Read the CSV file into a DataFrame
    df = pd.read_csv(FILENAME)
    # print(df.shape)

    # Extract unique sector names
    unique_sector_names = df["sector_name"].unique().tolist()
    # print(len(unique_sector_names))
    # print(unique_sector_names)
    df = pd.DataFrame(unique_sector_names, columns=["name"])

    # print(df)

    # df['sector_id'] = range(1, len(df) + 1)

    df.insert(0, "sector_ref", range(1, len(df) + 1))

    df.insert(2, "sector_code", "code")
    # Add a new column 'CREATED_AT' with current timestamp
    df["created_at"] = datetime.now()

    # print(df)

    # Get the underlying database engine
    engine = db.engine
    conn = engine.raw_connection()
    cursor = conn.cursor()

    # Load the DataFrame into the stock_master table
    df.to_sql("sector_master", conn, if_exists="append", index=False)

    # Commit the transaction and close the connection
    conn.commit()
    conn.close()

    return "sectors loaded", len(df[0])

# @bp.route("/create-test-users", methods=["GET"])
def create_test_users():
    print('create_test_users()')
      # Creating users:
    admin_role_id = (
        db.session.query(UserRole).filter(UserRole.name == "ADMIN").first().id
    )
    submitter_role_id = (
        db.session.query(UserRole).filter(UserRole.name == "SUBMITTER").first().id
    )
    
    print(admin_role_id, submitter_role_id)

    user_list = [
        User(
            fname="Charmi",
            lname="-",
            email="admin@gmail.com",
            password="11111",
            userrole_id=admin_role_id,
            isactive=1,
            amc_id=0,
            created_at=datetime.now(),
        ),
        User(
            fname="Ashraf",
            lname="-",
            email="admin2@gmail.com",
            password="11111",
            userrole_id=admin_role_id,
            isactive=1,
            amc_id=0,
            created_at=datetime.now(),
        ),
        User(
            fname="Aadya",
            lname="-",
            email="dmudgilfun@gmail.com",
            password="11111",
            userrole_id=submitter_role_id,
            isactive=1,
            amc_id=21,
            created_at=datetime.now(),
        ),
        User(
            fname="Charmi",
            lname="-",
            email="dmudgilmsg@gmail.com",
            password="11111",
            userrole_id=submitter_role_id,
            isactive=1,
            amc_id=105,
            created_at=datetime.now(),
        ),
        User(
            fname="Kamal",
            lname="-",
            email="dmudgil@gmail.com",
            password="11111",
            userrole_id=submitter_role_id,
            isactive=1,
            amc_id=20,
            created_at=datetime.now(),
        ),
    ]
    print(' adding users to list..')
    db.session.add_all(user_list)
    print('added to session')
    db.session.commit()
    print(' users stored...')
    
    return "loaded admin users"

# @bp.route("/load-amc-users", methods=["GET"])
def load_amc_users():
    

    # Construct the path to the XLS file
    FILE_NAME = os.path.join(current_dir, "init_data", "ListOfAMCUsers_nav.xlsx")    

    sheet_name = "AMC Users"
    
    # Read the Excel file, skipping the second row (index 1) which contains subheaders
    df = pd.read_excel(FILE_NAME, sheet_name=sheet_name)

    # Flatten the multi-level column names
    # df.columns = [f"{col[0]}_{col[1]}" if col[1] else col[0] for col in df.columns]

    # Rename columns to make them more readable
    df = df.rename(columns={
        'ID': 'ID',
        'amc_id': 'amc_id',
        'Name': 'Name',
        'POC 1_First Name': 'POC1_FirstName',
        'POC 1_Last Name': 'POC1_LastName',
        'POC 1_E-mail': 'POC1_Email',
        'POC 2_First Name': 'POC2_FirstName',
        'POC 2_Last Name': 'POC2_LastName',
        'POC 2_E-mail': 'POC2_Email',
        'POC 3_First Name': 'POC3_FirstName',
        'POC 3_Last Name': 'POC3_LastName',
        'POC 3_E-mail': 'POC3_Email',
        'POC 4_First Name': 'POC4_FirstName',
        'POC 4_Last Name': 'POC4_LastName',
        'POC 4_E-mail': 'POC4_Email',
        'POC 5_First Name': 'POC5_FirstName',
        'POC 5_Last Name': 'POC5_LastName',
        'POC 5_E-mail': 'POC5_Email',
        'POC 6_First Name': 'POC6_FirstName',
        'POC 6_Last Name': 'POC6_LastName',
        'POC 6_E-mail': 'POC6_Email'
    })

    # print(f" df = \n{df}")
    
    # df.to_csv('output_file.csv', index=False)
    
    # amc_dict = df_to_amc_dict(df)
    
    # print(f" amc_dict = {amc_dict}")
    
    final_df = convert(df)
    # final_df.to_csv('output_file.csv', index=False)
    # Usage example:
    load_users_to_database(final_df, submitter_id=2, p_password='11111')
    
    # store_amc_users(amc_dict)
    return " amc users loaded"    


def load_users_to_database(final_df, submitter_id, p_password):
    # Create engine and session

    users_to_insert = []
    users_to_update = []

    try:
        for _, row in final_df.iterrows():
            existing_user = db.session.query(User).filter_by(email=row['email']).first()
            
            if existing_user:
                # Update existing user
                existing_user.fname = row['first_name']
                existing_user.lname = row['last_name']
                existing_user.amc_id = row['amc_id']
                existing_user.isactive = 1
                existing_user.created_at = datetime.utcnow()
                users_to_update.append(existing_user)
            else:
                # Create new user
                new_user = User(
                    fname=row['first_name'],
                    lname=row['last_name'],
                    email=row['email'],
                    password=p_password,
                    userrole_id=submitter_id,
                    amc_id=row['amc_id'],
                    isactive=1,
                    created_at=datetime.utcnow()
                )
                users_to_insert.append(new_user)

        # Bulk insert new users
        if users_to_insert:
            db.session.bulk_save_objects(users_to_insert)

        # Bulk update existing users
        if users_to_update:
            db.session.bulk_save_objects(users_to_update, update_changed_only=True)

        # Commit the changes
        db.session.commit()

        print(f"Data loading completed. Inserted {len(users_to_insert)} new users and updated {len(users_to_update)} existing users.")

    except Exception as e:
        db.session.rollback()
        print(f"An error occurred: {str(e)}")
    finally:
        db.session.close()




def convert (df):
    
    # Assuming your original DataFrame is called 'df'

    # Step 1: Melt the DataFrame
    melted_df = pd.melt(df, 
                        id_vars=['ID', 'amc_id', 'amc_name'], 
                        value_vars=[col for col in df.columns if col.startswith('user')],
                        var_name='user_field', 
                        value_name='value')

    # Step 2: Create separate columns for fname, lname, email
    melted_df['field_type'] = melted_df['user_field'].str.split('_').str[-1]
    melted_df['user_number'] = melted_df['user_field'].str.extract('(\d+)')

    # Step 3: Pivot the melted DataFrame
    pivoted_df = melted_df.pivot_table(index=['ID', 'amc_id', 'amc_name', 'user_number'], 
                                    columns='field_type', 
                                    values='value', 
                                    aggfunc='first')

    # Step 4: Reset index and rename columns
    pivoted_df = pivoted_df.reset_index()
    pivoted_df.columns.name = None
    pivoted_df = pivoted_df.rename(columns={'fname': 'first_name', 'lname': 'last_name'})

    # Step 5: Replace empty strings with NaN, then replace NaN in first_name and last_name with '-'
    pivoted_df = pivoted_df.replace(r'^\s*$', np.nan, regex=True)
    pivoted_df['first_name'] = pivoted_df['first_name'].fillna('-')
    pivoted_df['last_name'] = pivoted_df['last_name'].fillna('-')

    # Step 6: Remove rows where email is null
    pivoted_df = pivoted_df.dropna(subset=['email'])

    # Step 7: Remove double quotes and commas from all columns
    for col in pivoted_df.columns:
        if pivoted_df[col].dtype == 'object':
            pivoted_df[col] = pivoted_df[col].str.replace('"', '', regex=False)
            pivoted_df[col] = pivoted_df[col].str.replace(',', '', regex=False)

    # Step 8: Drop unnecessary columns and reset index
    final_df = pivoted_df.drop(['ID', 'amc_name', 'user_number'], axis=1).reset_index(drop=True)

    # Display the result
    print(final_df)
    return final_df



# def store_amc_users(amc_dict):
#     print('store_amc_users()')
    
#     # print( len(amc_dict))
#     # print(amc_dict[0])
    
#     # first_key, first_value = next(iter(amc_dict.items()))
#     # print(f"First key: {first_key}, First value: {first_value}")

#     submitter_role_id = db.session.query(UserRole.id).filter(UserRole.name == "SUBMITTER").scalar()

#     users_to_insert = []
#     for amc_id, users in amc_dict.items():
#         print(" in for looooooppppp")
#         print(f"amc_id = {amc_id}")
#         for temp_user in users:
#             users_to_insert.append(User(
#                 fname=temp_user['user_fname'],
#                 lname=temp_user['user_lname'],
#                 email=temp_user['user_email'],
#                 password="11111",
#                 userrole_id=submitter_role_id,
#                 amc_id=amc_id,
#                 isactive=1,
#                 created_at=datetime.now(timezone.utc)
#             ))

#     # Bulk insert
#     try:
#         db.session.bulk_save_objects(users_to_insert)
#         db.session.commit()
#         print(f"Successfully inserted {len(users_to_insert)} users.")
#     except IntegrityError as e:
#         db.session.rollback()
#         print(f"Error inserting users: {str(e)}")
#         # Handle duplicate emails or other integrity errors
#         # You might want to update existing users or skip duplicates
#     except Exception as e:
#         db.session.rollback()
#         print(f"An error occurred: {str(e)}")
        


# def df_to_amc_dict(df):
#     print('df_to_amc_dict()')
    
#     amc_dict = {}
    
#     # Get all AMC IDs
#     amc_ids = df['amc_id'].unique()
    
#     for amc_id in amc_ids:
#         amc_df = df[df['amc_id'] == amc_id]
        
#         users = []
#         for i in range(1, 7):  # Assuming you have POC1 to POC6
#             user_data = amc_df[[f'user{i}_fname', f'user{i}_lname', f'user{i}_email']]
            
#             # Check if any field is not null
#             mask = user_data.notna().any(axis=1)
#             valid_users = user_data[mask]
            
#             users.extend([
#                 {
#                     'user_fname': row[f'user{i}_fname'] if pd.notna(row[f'user{i}_fname']) else '',
#                     'user_lname': row[f'user{i}_lname'] if pd.notna(row[f'user{i}_lname']) else '',
#                     'user_email': row[f'user{i}_email'] if pd.notna(row[f'user{i}_email']) else ''
#                 }
#                 for _, row in valid_users.iterrows()
#             ])
        
#         amc_dict[amc_id] = users
        
#         # print(amc_dict)
    
#     return amc_dict


# @bp.route("/populate-pms-nav", methods=["GET"])
def populate_pms_nav():
    print('populate-pms-nav()')
    try:
        # Drop the existing table and recreate it
        # db.session.execute(text("DROP TABLE IF EXISTS pms_nav;"))
        # db.session.commit()
        # db.create_all()

        # Construct the path to the CSV file
        FILE_NAME = os.path.join(current_dir, "init_data", "LastUpdatedNAV.csv")
        
        # # Read the CSV file
        # file_path = "init_data/LastUpdatedNAV.csv"
        user_id = 2 # For Ashraf
        # print('reading file')
        with open(FILE_NAME, "r") as file:
            csv_reader = csv.DictReader(file)
            ctr = 0
            for row in csv_reader:
                # print(row)
                # Parse the Nav Date
                nav_date = datetime.strptime(row['Nav Date'], '%d/%m/%Y')
                # print(nav_date)
                
                # Create a new PMSNav object
                pms_nav = PMSNav(
                    pms_id=int(row['Scheme Id']),
                    user_id=user_id,
                    p_month=nav_date.month,
                    p_year=nav_date.year,
                    nav = float(row['Nav']),
                    created_at=datetime.utcnow()
                )
                
                # print(pms_nav)
                # Add the object to the session
                db.session.add(pms_nav)
                crt = ctr + 1
        # Commit all changes to the database
        db.session.commit()
    

        return (
            jsonify(
                {
                    "message": f"PMSNav table populated with {ctr} entries."
                }
            ),
            200,
        )
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
    
    


# @bp.route("/load-dummy-pmsperf", methods=["GET"])
def dummy_pmsperf():
    print('dummy_pmsperf()')

    pms_records = PMSMaster.query.all()

    # Set fixed values for month and year
    p_month = 9  # September
    p_year = 2023

    # Dummy user_id (replace with appropriate value)
    user_id = 1

    for pms in pms_records:
        # Check if a record already exists for this PMS, month, and year
        existing_record = PMSPerformance.query.filter_by(
            pms_id=pms.pms_id,
            p_month=p_month,
            p_year=p_year
        ).first()

        if not existing_record:
            # Create a new PMSPerformance object with dummy data
            new_performance = PMSPerformance(
                pms_id=pms.pms_id,
                user_id=user_id,
                p_month=p_month,
                p_year=p_year,
                one_month=0.0,
                three_months=0.0,
                six_months=0.0,
                twelve_months=0.0,
                two_year_cagr=0.0,
                three_year_cagr=0.0,
                five_year_cagr=0.0,
                ten_year_cagr=0.0,
                cagr_si=0.0,
                si=0.0,
                created_at=datetime.utcnow()
            )
            
        # Add the new performance record to the session
        db.session.add(new_performance)              
            
    try:
        
        db.session.commit()
        print(f"Successfully inserted dummy records for {len(pms_records)} PMS entries.")
        
        return (
            jsonify(
                {
                    
                    "message": f"Successfully inserted dummy records for {len(pms_records)} PMS entries."
                }
            ),
            200,
        )
    except Exception as e:
        db.session.rollback()
        print(f"error: str(e)")
        return jsonify({"error": str(e)}), 500        
    


# @bp.route("/load-dummy-indexperf", methods=["GET"])
def dummy_indexperf():
    print('dummy_indexperf()')

    index_records = IndexMaster.query.all()

    # Set fixed values for month and year
    p_month = 9  # September
    p_year = 2023

    # Dummy user_id (replace with appropriate value)
    user_id = 1
    ctr = 0

    for rec in index_records:
        
        # print(rec.id, rec.index_code, rec.name)
        ctr = ctr + 1
        # Check if a record already exists for this PMS, month, and year
        # existing_record = IndexPerformance.query.filter_by(
        #     pms_id=pms.pms_id,
        #     p_month=p_month,
        #     p_year=p_year
        # ).first()
        existing_record = False
        if not existing_record:
            # print('not existing is true!!!')
            # Create a new PMSPerformance object with dummy data
            new_performance = IndexPerformance(
            user_id=user_id,
            index_id=rec.id,
            p_month=p_month,
            p_year=p_year,
            one_month=0.0,
            three_months=0.0,
            six_months=0.0,
            twelve_months=0.0,
            two_year_cagr=0.0,
            three_year_cagr=0.0,
            five_year_cagr=0.0,
            ten_year_cagr=0.0,
            created_at=datetime.utcnow(),
        )
        
        # print(type(new_performance))
        # Add the new performance record to the session
        db.session.add(new_performance)              
            
    try:
        
        db.session.commit()
        print(f"Successfully inserted dummy records for {ctr} PMS entries.")
        
        return (
            jsonify(
                {
                    
                    "message": f"Successfully inserted dummy records for {ctr} PMS entries."
                }
            ),
            200,
        )
    except Exception as e:
        db.session.rollback()
        print(f"error: str(e)")
        return jsonify({"error": str(e)}), 500     
    
# @bp.route("/load-dummy-stock", methods=["GET"])
def loadDummyStock():
    print("loadDummyStock()")
    dummy_record = [
        StockMaster(1, "Dummy Stock", "DUMMY","DUMMY", datetime.now()),
        
    ]
    db.session.add_all(dummy_record)
    db.session.commit()
    # print("Loaded DummyStock")
    # print("_______________________")
    return "Loaded DummyStock"

# @bp.route("/load-dummy-sector", methods=["GET"])
def loadDummySector():
    print("loadDummySector()")
    dummy_record = [
        SectorMaster(1, "DUMMY Sector", "DUMMY", datetime.now()),
        
    ]
    db.session.add_all(dummy_record)
    db.session.commit()
    # print("Loaded DummySector")
    # print("_______________________")
    
    return "Loaded DummySector"


# @bp.route("/load-dummy-pmsstocks", methods=["GET"])
def loadDummyPmsStocks():
    
    print("loadDummyPmsStocks()")
    dummy_stock_id = (
        db.session.query(StockMaster).filter(StockMaster.stock_symbol == "DUMMY").first().id
    )
    
    pms_records = PMSMaster.query.all()


    for pms in pms_records:
        # Check if a record already exists for this PMS, month, and year
        existing_record = PMSStock.query.filter_by(
            pms_id=pms.pms_id,
            stock_id=dummy_stock_id

        ).first()
        # existing_record = False
        if not existing_record:
            # Create a new PMSPerformance object with dummy data
            dummy_record = PMSStock(
                pms_id=pms.pms_id,
                stock_id = dummy_stock_id,
                pct_deployed = 0,
                created_at=datetime.utcnow()
            )
            
        # Add the new performance record to the session
        db.session.add(dummy_record)              
            
    try:
        
        db.session.commit()
        print(f"Successfully inserted dummy stock record for {pms.pms_id}")
        
        return (
            jsonify(
                {
                    
                    "message": f"Successfully inserted dummy stock record for {pms.pms_id}"
                }
            ),
            200,
        )
    except Exception as e:
        db.session.rollback()
        print(f"error: str(e)")
        return jsonify({"error": str(e)}), 500        



# @bp.route("/load-dummy-pmssector", methods=["GET"])
def loadDummyPmsSectors():
    print("loadDummyPmsSectors()")
    
    # print("loadDummyPmsSectors()")
    dummy_sector_id = (
        db.session.query(SectorMaster).filter(SectorMaster.sector_code == "DUMMY").first().id
    )
    
    pms_records = PMSMaster.query.all()


    for pms in pms_records:
        # Check if a record already exists for this PMS, month, and year
        existing_record = PMSStock.query.filter_by(
            pms_id=pms.pms_id,
            stock_id=dummy_sector_id

        ).first()
        # existing_record = False
        if not existing_record:
            # Create a new PMSPerformance object with dummy data
            dummy_record = PMSSector(
                pms_id=pms.pms_id,
                sector_id = dummy_sector_id,
                pct_deployed = 0,
                created_at=datetime.utcnow()
            )
            
        # Add the new performance record to the session
        db.session.add(dummy_record)              
            
    try:
        
        db.session.commit()
        print(f"Successfully inserted dummy sector record for {pms.pms_id}")
        
        return (
            jsonify(
                {
                    
                    "message": f"Successfully inserted dummy sector record for {pms.pms_id}"
                }
            ),
            200,
        )
    except Exception as e:
        db.session.rollback()
        print(f"error: str(e)")
        return jsonify({"error": str(e)}), 500        
