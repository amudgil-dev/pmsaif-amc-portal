

from app.models.models import AMCMaster, PMSMaster, PMSStock, User, db
from sqlalchemy import text
from pandas import DataFrame
import pandas as pd
from pandas.tseries.offsets import MonthEnd
from flask import current_app

from app.helpers.helper_util import generate_range

def getPmsListing(user_id):
    print('getPmsListing()')
    # print(user_id)
    # print(' 999999')
    
    query = 'select t1.amc_id amc_id, t1.name amc_name, t2.name pms_name, t2.pms_id pms_id, t2.index_id index_id, t3.name index_name   '\
            ' from amc_master t1 , pms_master t2 , index_master t3  '\
            '  where t1.amc_id =   '\
            ' (select amc_id from user where id = '+str(user_id)+')  '\
            ' and t1.amc_id = t2.amc_id ' \
            ' and t2.index_id = t3.id '
    
    
    label_tuple = ('amc_id', 'amc_name', 'pms_name', 'pms_id', 'index_id', 'index_name')    


    try:

        with current_app.app_context():
            
            with db.engine.connect() as connection:
 
                result = connection.execute(text(query), {"user_id": user_id})
                records = result.fetchall()
  
            pms_array = [dict(zip(label_tuple, row)) for row in records]
     
            # print(pms_array)
            return pms_array
    except Exception as e:
        print(f"in getPmsListing() exception : {e}" )
        current_app.logger.error(f"Error in getPmsListing: {e}")
        
        return None    

def getAdminPmsListing(amc_id):
    print('getAdminPmsListing()')
    print(amc_id)
    
    query = 'select t1.amc_id amc_id, t1.name amc_name, t2.name pms_name, t2.pms_id pms_id, t2.index_id index_id, t3.name index_name   '\
            ' from amc_master t1 , pms_master t2 , index_master t3  '\
            '  where t1.amc_id =   '+str(amc_id) +' '\
            ' and t1.amc_id = t2.amc_id ' \
            ' and t2.index_id = t3.id '
    
    
    label_tuple = ('amc_id', 'amc_name', 'pms_name', 'pms_id', 'index_id', 'index_name')    


    try:

        with current_app.app_context():
            
            with db.engine.connect() as connection:
 
                result = connection.execute(text(query), {"amc_id": amc_id})
                records = result.fetchall()
  
            pms_array = [dict(zip(label_tuple, row)) for row in records]
     
            print(f"pms_array : {pms_array}")
            return pms_array
    except Exception as e:
        print(" getAdminPmsListing () IN EXCEPTION")
        print(f"in getPmsListing() exception : {e}" )
        current_app.logger.error(f"Error in getPmsListing: {e}")
        
        return None    
    



def getAdminPmsListingByIndex(index_id):
    print('getAdminPmsListingByIndex()')
    print(index_id)
    
    query = 'select t1.amc_id amc_id, t1.name amc_name, t2.name pms_name, t2.pms_id pms_id, t2.index_id index_id, t3.name index_name   '\
            ' from amc_master t1 , pms_master t2 , index_master t3  '\
            '  where t2.index_id =   '+str(index_id) +' '\
            ' and t1.amc_id = t2.amc_id ' \
            ' and t2.index_id = t3.id '
    
    
    label_tuple = ('amc_id', 'amc_name', 'pms_name', 'pms_id', 'index_id', 'index_name')    


    try:

        with current_app.app_context():
            
            with db.engine.connect() as connection:
 
                result = connection.execute(text(query), {"index_id": index_id})
                records = result.fetchall()
  
            pms_array = [dict(zip(label_tuple, row)) for row in records]
     
            # print(f"pms_array : {pms_array}")
            return pms_array
    except Exception as e:
        print(" getAdminPmsListing () IN EXCEPTION")
        print(f"in getPmsListing() exception : {e}" )
        current_app.logger.error(f"Error in getPmsListing: {e}")
        
        return None    
    
    
def getUserListing(amc_id):
    print('getUserListing()')
    
    query = 'select t1.id user_id,t1.fname fname, t1.lname lname, t1.email email, t1.isactive isactive, t1.amc_id amc_id   '\
            ' from user t1   '\
            '  where t1.amc_id =   '+str(amc_id) +' '\
    
    
    label_tuple = ('user_id','fname', 'lname', 'email', 'isactive', 'amc_id')    


    try:

        with current_app.app_context():
            
            with db.engine.connect() as connection:
 
                result = connection.execute(text(query), {"amc_id": amc_id})
                records = result.fetchall()
  
            user_array = [dict(zip(label_tuple, row)) for row in records]
     
            # print(user_array)
            return user_array
    except Exception as e:
        print(f"in getUserListing() exception : {e}" )
        current_app.logger.error(f"Error in getUserListing: {e}")
        
        return None    
    
    
def getAmcListing():
    print('getAmcListing()')
    
    query = 'select t1.amc_id amc_id, t1.name amc_name   '\
            ' from amc_master t1 order by t1.amc_id  '
    
    
    label_tuple = ('amc_id', 'amc_name')    


    try:

        with current_app.app_context():
            
            with db.engine.connect() as connection:
 
                result = connection.execute(text(query))
                records = result.fetchall()
  
            amc_array = [dict(zip(label_tuple, row)) for row in records]
     
            # print(pms_array)
            return amc_array
    except Exception as e:
        print(f"in getAmcListing() exception : {e}" )
        current_app.logger.error(f"Error in getAmcListing: {e}")
        
        return None    
    


def getPmsDashDataList(pms_id):
    print('getPmsDashDataList()')
    print("pms_id ==>", pms_id)
    
    pms_perf, pms_label = getPmsPerformance(pms_id)
    
    
    print(f" type(pms_perf) ====>><<<<< {type(pms_perf)} and {pms_perf}")
    index_perf, index_label = getPmsIndexPerformance(pms_id, pms_perf['month'], pms_perf['year'])
    
    pms_details = getPmsDetails(pms_id)
    pms_stocks = getPmsStocks(pms_id)
    pms_sectors = getPmsSectors(pms_id)

    return pms_perf,index_perf,pms_details, pms_stocks, pms_sectors

def getPmsPerformance(pms_id):
    print('getPmsPerformance()')
    query = '' \
        'select t2.id perf_id, t4.name amc_name,t2.pms_id pms_id, t1.name pms_name, t1.index_id index_id, t3.name index_name , '\
        ' t2.p_month month, t2.p_year year,one_month, three_months,six_months,twelve_months,two_year_cagr,three_year_cagr,five_year_cagr,ten_year_cagr,cagr_si,si '\
        ' from pms_master t1 , pms_performance t2 , index_master t3 , amc_master t4 '\
        ' where t1.pms_id = t2.pms_id '\
        ' and t1.index_id = t3.id '\
        ' and t4.amc_id = t1.amc_id '\
        ' and t2.pms_id =  '+ str(pms_id) +''\
        ' order by year desc, month desc, t2.id desc limit 1'
    
    label_pms_perf = ('perf_id','amc_name','pms_id', 'pms_name', 'index_id', 'index_name', 'month', 'year', 'one_month', 'three_months', 'six_months', 'twelve_months', 'two_year_cagr', 'three_year_cagr', 'five_year_cagr', 'ten_year_cagr', 'cagr_si', 'si') 

    # sql = text(query)
    # records = db.session.execute(sql)

    # tuple_list = [i for i in records]

    # tuple = tuple_list[0]
    # pms_perf = tuple

    try:
        with current_app.app_context():
            with db.engine.connect() as connection:
                result = connection.execute(text(query), {"pms_id": pms_id})
                records = result.fetchall()

            # pms_perf = [zip(label_pms_perf, row) for row in records][0]
            tuple_list = [i for i in records]

            tuple = tuple_list[0]
            pms_perf = tuple            
            
            
            
            # print(f" before converting to dicationary {pms_perf }")
            # pms_dict = dict(pms_perf)
            # pms_dict = {str(i): value for i, value in enumerate(pms_perf)}      
            pms_dict = dict(zip(label_pms_perf, pms_perf))      
            # print(f" converted to dicationary {pms_dict}")
            # pms_perf = pms_perf[0]
            # print(f"pms_perf =====> {type(pms_perf)}")
            return pms_dict ,label_pms_perf
    except Exception as e:
        current_app.logger.error(f"Error in getPmsListing: {e}")
        return None , None 

    # return pms_perf , label_pms_perf


def getPmsIndexPerformance(pms_id,month, year):
    print('getPmsIndexPerformance()')
    
    # print(f" pms_id={pms_id}, month={month}  year={year} ")
    query = text("""
        SELECT t2.id, t1.name AS index_name, t2.index_id,
               t2.p_month AS month, t2.p_year AS year,
               one_month, three_months, six_months, twelve_months,
               two_year_cagr, three_year_cagr, five_year_cagr, ten_year_cagr
        FROM index_performance t2
        JOIN index_master t1 ON t1.id = t2.index_id
        WHERE t2.index_id = (SELECT index_id FROM pms_master WHERE pms_id = :pms_id)
          AND t2.p_month = :month AND t2.p_year = :year
        ORDER BY year DESC, month DESC, t2.id DESC
        LIMIT 1
    """)

    params = {'pms_id': pms_id, 'month': month, 'year': year}

    label_index_perf = ('id', 'index_name', 'index_id', 'month', 'year', 'one_month', 'three_months', 
                        'six_months', 'twelve_months', 'two_year_cagr', 'three_year_cagr', 
                        'five_year_cagr', 'ten_year_cagr')

    try:
        with current_app.app_context():
            with db.engine.connect() as connection:
                result = connection.execute(query, params)
                records = result.fetchall()
                tuple_list = list(records)


    # query = ' select t2.id, t1.name index_name, t2.index_id index_id, '\
    #     ' t2.p_month month, t2.p_year year,one_month, three_months,six_months,twelve_months,two_year_cagr,three_year_cagr,five_year_cagr,ten_year_cagr '\
    #     ' from index_performance t2, index_master t1 '\
    #     ' where t1.id = t2.index_id '\
    #     ' and t2.index_id = (select index_id from pms_master where pms_id = '+str(pms_id)+') '\
    #     ' and t2.p_month = '+str(month)+' and t2.p_year = '+str(year)+' '\
    #     ' order by year desc, month desc, t2.id desc limit 1' 
    
    # print(f"query = {query}")
    
    # label_index_perf = ('id','index_name', 'index_id', 'month', 'year', 'one_month', 'three_months', 'six_months', 'twelve_months', 'two_year_cagr', 'three_year_cagr', 'five_year_cagr', 'ten_year_cagr')

    # try:
    #     with current_app.app_context():
    #         with db.engine.connect() as connection:
    #             result = connection.execute(text(query))
    #             records = result.fetchall()
                
    #             tuple_list = [i for i in records]
    except Exception as e:
        print('Exception occured ')
        print(e)
        pass
    
    # print(tuple_list)
    # print(type(tuple_list))
    # print(len(tuple_list))


    if len(tuple_list) >= 1:
        print('Index perf record found')
        index_perf_tuple = tuple_list[0]
    else:
        print('No Records found generating zero value index records...')
        index_perf_tuple = (
            0,              # id
            'Dummy Index',             # index_name
            0,              # index_id
            month,           # month
            year,         # year
            0.0,            # one_month
            0.0,            # three_months
            0.0,            # six_months
            0.0,            # twelve_months
            0.0,            # two_year_cagr
            0.0,            # three_year_cagr
            0.0,            # five_year_cagr
            0.0             # ten_year_cagr
        )

    index_perf = index_perf_tuple
    
    index_perf = dict(zip(label_index_perf, index_perf))      
    
    return index_perf , label_index_perf

def getIndexPerformance(index_id):
    print('getIndexPerformance()')

    query = ' select t2.id,t1.name index_name, t2.index_id index_id, '\
        ' t2.p_month month, t2.p_year year,one_month, three_months,six_months,twelve_months,two_year_cagr,three_year_cagr,five_year_cagr,ten_year_cagr '\
        ' from index_performance t2, index_master t1 '\
        ' where t1.id = t2.index_id '\
        ' and t2.index_id = '+str(index_id)+' '\
        ' order by year desc, month desc, t2.id desc limit 100 ' 
    
    # print('------')
    # print( query)
    # print('------')
    
    label_index_perf = ('id','index_name', 'index_id', 'month', 'year', 'one_month', 'three_months', 'six_months', 'twelve_months', 'two_year_cagr', 'three_year_cagr', 'five_year_cagr', 'ten_year_cagr')

    sql = text(query)
    records = db.session.execute(sql)
    # print(records)
    print(type(records))

    # Convert the result to a list
    result_list = list(records)

    # Check if the list is empty
    if not result_list:
        return None
    else:
        return result_list

        
 

def getPmsDetails(pms_id):
    print('getPmsDetails()')

    query = ' select '\
            ' t1.id pms_internal_id, t1.name pms_name, stocks_min min, stocks_max max, aum ,portfolio_pe, large_cap, mid_cap, small_cap, cash, t2.name index_name '\
            ' from pms_master t1 , index_master t2'\
            ' where pms_id = '+str(pms_id) + ''\
            ' and t1.index_id = t2.id '
    
    labels = ('pms_internal_id', 'pms_name', 'min', 'max', 'aum', 'portfolio_pe', 'large_cap', 'mid_cap', 'small_cap', 'cash') 

    try:
        with current_app.app_context():
            with db.engine.connect() as connection:
                result = connection.execute(text(query), {"pms_id": pms_id})
                records = result.fetchall()
                
                tuple_list = [i for i in records]
                tuple = tuple_list[0]
                pms_details = tuple
                pms_details = dict(zip(labels, pms_details))   
                return pms_details

    except:
        None




def getPmsStocks(pms_id):
    print('getPmsStocks()')

    query = ' select ' \
            ' t1.pct_deployed , t2.name stock_name ,t1.stock_id stock_id,t2.stock_symbol, t2.isin_code'\
            ' from pms_stock t1, stock_master t2 '\
            ' where t1.stock_id = t2.id '\
            ' and t1.pms_id ='+ str(pms_id) 
                

    try:
        with current_app.app_context():
            with db.engine.connect() as connection:
                result = connection.execute(text(query), {"pms_id": pms_id})
                records = result.fetchall()
                
                tuple_list = [i for i in records]
                pms_stocks = tuple_list
                
                return pms_stocks

    except:
        None



def getPmsSectors(pms_id):
    print('getPmsSectors()')

    query = ' select '\
            ' t1.pct_deployed , t2.name sector_name ,t1.sector_id sector_id, t2.sector_code'\
            ' from pms_sector t1, sector_master t2 '\
            ' where t1.sector_id = t2.id '\
            ' and t1.pms_id = '+str(pms_id)
                

    try:
        with current_app.app_context():
            with db.engine.connect() as connection:
                result = connection.execute(text(query), {"pms_id": pms_id})
                records = result.fetchall()
                
                tuple_list = [i for i in records]
                pms_sectors = tuple_list
                
                return pms_sectors

    except:
        None




def checkEntitlementsFromDB(user_id, pms_id):
    print('checkEntitlementsFromDB()')

    try:
        # Use parameterized query to prevent SQL injection
        query = text("""
            SELECT COUNT(*) as count 
            FROM user u
            JOIN pms_master pm ON u.amc_id = pm.amc_id
            WHERE u.id = :user_id AND pm.pms_id = :pms_id
        """)

        result = db.session.execute(query, {'user_id': user_id, 'pms_id': pms_id})
        count = result.scalar()

        authorized = count > 0

        current_app.logger.info(f"User {user_id} authorization for PMS {pms_id}: {authorized}")
        
        return authorized

    except Exception as e:
        current_app.logger.error(f"Error checking user entitlement: {str(e)}")
        return False
    
    

def getUserByUserId(user_id):
    return User.query.filter_by(id=user_id).first()
    
def getPmsOfAmc(amc_id):
    return PMSMaster.query.filter_by(amc_id=amc_id).all()
    
    # delete all the records from the pms_stocks table for given pms_id
def deletePmsStocks(pms_id):
    print('deletePmsStocks()')
    print("pms_id ==>", pms_id)
    # delete_query = 'delete from pms_stock where pms_id = ' + str(pms_id)
    # delete_query = 'delete from pms_stock where pms_id = ' + str(pms_id)
    query = "delete from pms_stock where pms_id = :pms_id"

    try:
        result = db.session.execute(text(query), {'pms_id': pms_id})
        # db.session.commit()
        print(f"Deleted {result.rowcount} rows from pms_stock")
        return True
    except Exception as e:
        db.session.rollback()
        print(f"Error deleting PMS stocks: {str(e)}")
        return False
        


# def deletePmsSectors(pms_id):
#     print('deletePmsSectors()')
#     print("pms_id ==>", pms_id)
#     # delete_query = 'delete from pms_stock where pms_id = ' + str(pms_id)
#     # delete_query = 'delete from pms_stock where pms_id = ' + str(pms_id)
#     query = text("delete from pms_sector where pms_id = :pms_id")
    
#     try:
#         result = db.session.execute(text(query), {'pms_id': pms_id})
#         # db.session.commit()
#         print(f"Deleted {result.rowcount} rows from pms_stock")
#         return True
#     except Exception as e:
#         db.session.rollback()
#         print(f"Error deleting PMS stocks: {str(e)}")
#         return False
        

def getIndexListing():
    print('getIndexListing()')
    
    query = 'select t1.id id, t1.index_ref, t1.name index_name, t1.index_code    '\
            ' from  index_master t1  '
    

    sql = text(query)
    records = db.session.execute(sql)
    # print(records)

    tuple_list = [i for i in records]
    index_list = tuple_list
    # print('...........')
    # print(len(index_list))
    for tuple in index_list:
        print(tuple)

    # print('...........')
    return index_list



def getPerformanceReport(month, year):
    print('getPerformanceReport()')
    
    df_pms_perf = getPMSPerfDF(month, year )
    df_index_perf = getIndexPerfDF(month, year)



    merged_df = pd.merge(df_pms_perf, df_index_perf, on='index_id', how='outer')


    merged_df = merged_df.sort_values(
        by=['amc_id', 'pms_id'],
        ignore_index=True
    )
    
    merged_df = merged_df.drop(columns=['index_id'], axis=1)
    merged_df = merged_df.rename(columns={
                            'amc_id': 'Company Id',
                            'pms_id': 'Scheme ID'
                            
                            })   

    # shifting column positions

    popped = merged_df.pop('Company Name')
    merged_df.insert(0, 'Company Name', popped)
    
    popped = merged_df.pop('Scheme Name')
    merged_df.insert(1, 'Scheme Name', popped)
    
    popped = merged_df.pop('No. of stocks')
    merged_df.insert(6, 'No. of stocks', popped)    
    
    popped = merged_df.pop('AUM')
    merged_df.insert(12, 'AUM', popped)        
    
    # df3 = merged_df
    
    # Calculating the outperformance.
    # print("before ...")
    # print(merged_df.keys())
    
    merged_df['Out Performance'] = (merged_df['SI'] - merged_df ['Benchmark Since Inception']).round(2)
    
    # print("after ...")
    # print(merged_df.keys())
    # print(merged_df['Out Performance'])
    
    popped = merged_df.pop('Out Performance')
    merged_df.insert(22, 'Out Performance', popped)            
    
    popped = merged_df.pop('Benchmark Since Inception')
    merged_df.insert(31, 'Benchmark Since Inception',popped)         

    return merged_df


def getPMSPerfDF(month, year):
    # print('getPMSPerfDF()')
    
    # query = 'select   '\



    query = 'select *   '\
            ' from  amc_master t1 '\
            ' where amc_id > 0'

    sql = text(query)
    records = db.session.execute(sql)
    df_amc = pd.DataFrame(records.fetchall(), columns=records.keys())
    df_amc = df_amc.drop(columns=['id','created_at'], axis=1)
    df_amc = df_amc.rename(columns={'name': 'Company Name'}) 

    query = 'select *   '\
            ' from  pms_master t1 '\
            
    sql = text(query)
    records = db.session.execute(sql)
    df_pms = pd.DataFrame(records.fetchall(), columns=records.keys())
    df_pms.drop(columns=['id','created_at'], axis=1,inplace=True)
    df_pms = df_pms.rename(columns={
                                    'name': 'Scheme Name',
                                    'portfolio_pe': 'PE' ,
                                    'aum': 'AUM',
                                    'large_cap': 'Large',
                                    'mid_cap': 'Mid',
                                    'small_cap': 'Small',
                                    'cash': 'cash'                           
                                    }) 

    # creating new column from min and max to show range

    df_pms['No. of stocks'] = df_pms.apply(generate_range, axis=1)

    # removing the columns min and max
    popped = df_pms.pop('stocks_min')
    popped = df_pms.pop('stocks_max')

    # popping the Stocks column and inserting it into correct place
    popped = df_pms.pop('No. of stocks')
    df_pms.insert(3, 'No. of stocks', popped)

    print(f"df_pms.keys() after No of Stocks => {df_pms.keys()}")
    

    # popping the AUM column and inserting it into correct place after cash
    popped = df_pms.pop('AUM')
    df_pms.insert(10, 'AUM', popped)
    
    # print('Before Adding Category...',df_pms.keys())    
    
    
    # Adding Structure and Category column
    
    # df_pms["Category"] = 3
    # df_pms["Structure"] = 1    
    
    df_pms = df_pms.rename(columns={'structure_id': 'Structure ID'}) 
    df_pms = df_pms.rename(columns={'category_id': 'Category Id'})     
    
    # print('After adding structure ', df_pms.keys())    
        
    # popping the Category and Structure column and inserting it into correct place after Scheme ID
    popped = df_pms.pop('Category Id')
    df_pms.insert(3, 'Category Id', popped)
        
    popped = df_pms.pop('Structure ID')
    df_pms.insert(4, 'Structure ID', popped)    
    
    # print(df_pms.keys())    
    
    
    query = 'select *   '\
            ' from  pms_performance t1  '\
            ' where p_month = '+str(month)+' '\
            ' and p_year = '+str(year)+''
    
    sql = text(query)

    # print(sql)
    records = db.session.execute(sql)
    df_pms_perf = pd.DataFrame(records.fetchall(), columns=records.keys())
    df_pms_perf = df_pms_perf.drop(columns=['id','created_at','user_id','p_month','p_year'], axis=1)
    df_pms_perf = df_pms_perf.rename(columns={
                                    'one_month': '1m',
                                    'three_months': '3m',
                                    'six_months': '6m',
                                    'twelve_months': '1y',
                                    'two_year_cagr': '2y',
                                    'three_year_cagr': '3y',
                                    'five_year_cagr': '5y',
                                    'ten_year_cagr': '10 yrs',
                                    'cagr_si': 'SI',
                                    'si': 'Benchmark Since Inception'                                   
                                    })     


    df_pms_amc = pd.merge( df_amc,df_pms, on='amc_id', how='outer')


    df = pd.merge(df_pms_amc, df_pms_perf, on='pms_id', how='outer')


    # print('.....PMS PERF......')
    # print(df.keys() )
    # print(df['name_x'] )
    # print(df['name_y'] )
    # print('...........')
    return df


def getIndexPerfDF(month, year):
    # print('getIndexPerfDF()')
    # print( month, year)

    query = 'select *   '\
            ' from  index_master t1 '\
            
    sql = text(query)
    records = db.session.execute(sql)
    df_index = pd.DataFrame(records.fetchall(), columns=records.keys())
    df_index.drop(columns=['created_at','index_code','index_ref'], axis=1,inplace=True)
    df_index = df_index.rename(columns={'name': 'Index','id':'index_id'}) 

    # print(df_index.keys())

    
    query = 'select *   '\
            ' from  index_performance t1  '\
            ' where p_month = '+str(month)+' '\
            ' and p_year = '+str(year)+''
    
    sql = text(query)
    # print(sql)
    records = db.session.execute(sql)
    df_idx_perf = pd.DataFrame(records.fetchall(), columns=records.keys())
    # print(df_idx_perf)
    df_idx_perf = df_idx_perf.drop(columns=['id','created_at','user_id','p_month','p_year'], axis=1)
    df_idx_perf = df_idx_perf.rename(columns={
                                    'one_month': '1 Month Benchmark',
                                    'three_months': '3 Month Benchmark',
                                    'six_months': '6 Month Benchmark',
                                    'twelve_months': '1 Year Benchmark',
                                    'two_year_cagr': '2 Year Benchmark',
                                    'three_year_cagr': '3 Year Benchmark',
                                    'five_year_cagr': '5 Year Benchmark',
                                    'ten_year_cagr': '10 Year Benchmark'
                                    
                                                                       
                                    })     

    # print(df_idx_perf.keys())

    df = pd.merge( df_index,df_idx_perf, on='index_id', how='outer')
    # print(df.keys())
    
    # print('before popping Index', df.keys())
    # popping the Index column and inserting it into correct place
    popped = df.pop('Index')
    
    # print('after popping Index', df.keys())
    
    df.insert(9, 'Index', popped)
    
    # print('after re-inserting Index', df.keys())    

    # print('..... INDEX PERF ......')
    # print(df.head(10)  )
    # print('...........')
    return df


def getPmsNavDataList(pms_id):
    # print('getPmsNavDataList()')
    # print("pms_id ==>", pms_id)
    
    # pms_perf, pms_label = getPmsPerformance(pms_id)
    # index_perf, index_label = getPmsIndexPerformance(pms_id, pms_perf.month, pms_perf.year)
    
    pms_details = getPmsDetails(pms_id)
    pms_nav = getPmsDetails(pms_id)    
    # pms_stocks = getPmsStocks(pms_id)
    # pms_sectors = getPmsSectors(pms_id)

    return pms_details, pms_nav

def getAllStocks():
    print('getAllStocks()')

    query = ' select '\
            ' t1.id id , t1.stock_ref stock_ref, t1.name stock_name, t1.stock_symbol stock_symbol, t1.isin_code isin_code'\
            ' from stock_master t1 '
                
    try:
        with current_app.app_context():
            with db.engine.connect() as connection:
                result = connection.execute(text(query))
                records = result.fetchall()
                
                tuple_list = [i for i in records]
                stocks_list = tuple_list
                
                return stocks_list

    except Exception as e:
        print(f"An error occurred: {e}")
        return None



def getMostRecentNavReport():
    print('getMostRecentNavReport()')

    query = '''
                WITH ranked_nav AS (
                    SELECT *,
                        ROW_NUMBER() OVER (PARTITION BY pms_id ORDER BY p_year DESC, p_month DESC) as rn
                    FROM pms_nav
                )
                SELECT 
                    COALESCE(am.id, 0) AS amc_id,  -- Include amc_id in the SELECT statement
                    COALESCE(am.name, 'No AMC') AS Company,
                    pm.name AS Scheme,
                    pm.pms_id AS "Scheme Id",
                    CASE 
                        WHEN rn.p_year IS NOT NULL AND rn.p_month IS NOT NULL 
                        THEN date(rn.p_year || '-' || printf('%02d', rn.p_month) || '-01') 
                        ELSE NULL 
                    END AS "Nav Date",
                    rn.nav AS Nav

                FROM PMS_Master pm
                LEFT JOIN AMC_Master am ON pm.amc_id = am.amc_id
                LEFT JOIN ranked_nav rn ON pm.id = rn.pms_id AND rn.rn = 1
                ORDER BY 
                    COALESCE(am.id, 0),  -- Sort by amc_id first, using 0 for NULL values
                    pm.pms_id              -- Then sort by scheme name
        '''
    try:
        with current_app.app_context():
            with db.engine.connect() as connection:
                result = connection.execute(text(query))
                
                # Fetch the column names
                columns = result.keys()
                
                # Fetch all records
                records = result.fetchall()
                
                # Create DataFrame
                df = pd.DataFrame(records, columns=columns)
                
                # Convert 'Nav Date' to datetime
                df['Nav Date'] = pd.to_datetime(df['Nav Date'])
                
                # Convert 'Nav Date' to datetime, coercing errors to NaT
                df['Nav Date'] = pd.to_datetime(df['Nav Date'], errors='coerce')

                # Get the last day of the month for each date
                df['Nav Date'] = df['Nav Date'] + MonthEnd(0)

                # Define a function to format dates, returning a blank string for NaT values
                def format_date(date):
                    return date.strftime('%d-%b-%Y') if pd.notnull(date) else ''

                # Apply the formatting function to the 'Nav Date' column
                df['Nav Date'] = df['Nav Date'].apply(format_date)

                # Replace NaN values in the 'Nav' column with blank strings
                df['Nav'] = df['Nav'].fillna('')
                
                return df

    except Exception as e:
        print(f"An error occurred: {e}")
        return None