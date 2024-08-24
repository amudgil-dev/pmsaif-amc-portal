

from app.models.models import AMCMaster, PMSMaster, PMSStock, db
from sqlalchemy import text
from pandas import DataFrame
import pandas as pd
from flask import current_app

from app.helpers.helper_util import generate_range

def getPmsListing(user_id):
    print('getPmsListing()')
    
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
            
            print(pms_array)
            return pms_array
    except Exception as e:
        current_app.logger.error(f"Error in getPmsListing: {e}")
        return None    

    # sql = text(query)
    # records = db.engine.execute(sql)
    # print(records)

    # #iterate through object and create seperate arrays to be rendered by highcharts
    # pms_array = []

    # tuple_list = [i for i in records]
    # for row in tuple_list:
    #     pms_array.append(dict(zip(label_tuple, row)))
    
    # print(pms_array)

    # return pms_array






def getPmsDashDataList(pms_id):
    print('getPmsDashDataList()')
    print("pms_id ==>", pms_id)
    
    pms_perf, pms_label = getPmsPerformance(pms_id)
    index_perf, index_label = getPmsIndexPerformance(pms_id, pms_perf.month, pms_perf.year)
    
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

    sql = text(query)
    records = db.engine.execute(sql)
    
    print(records)

    #iterate through object and create seperate arrays to be rendered by highcharts
    # pms_perf = []

    tuple_list = [i for i in records]
    # for row in tuple_list:
    #     # pms_perf.append(dict(zip(label_pms_perf, row)))
    #     pms_perf.append(zip(label_pms_perf, row))
    print("----****????????*** ---")    
    print(tuple_list)
    tuple = tuple_list[0]
    print(tuple.pms_id)
    pms_perf = tuple

    return pms_perf , label_pms_perf


def getPmsIndexPerformance(pms_id,month, year):
    print('getPmsIndexPerformance()')

    query = ' select t2.id, t1.name index_name, t2.index_id index_id, '\
        ' t2.p_month month, t2.p_year year,one_month, three_months,six_months,twelve_months,two_year_cagr,three_year_cagr,five_year_cagr,ten_year_cagr '\
        ' from index_performance t2, index_master t1 '\
        ' where t1.id = t2.index_id '\
        ' and t2.index_id = (select index_id from pms_master where pms_id = '+str(pms_id)+') '\
        ' and t2.p_month = '+str(month)+' and t2.p_year = '+str(year)+' '\
        ' order by year desc, month desc, t2.id desc limit 1' 
    
    label_index_perf = ('id','index_name', 'index_id', 'month', 'year', 'one_month', 'three_months', 'six_months', 'twelve_months', 'two_year_cagr', 'three_year_cagr', 'five_year_cagr', 'ten_year_cagr')

    sql = text(query)
    records = db.engine.execute(sql)
    # print(records)

    tuple_list = [i for i in records]
    if len(tuple_list) > 1:
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
    return index_perf , label_index_perf

def getIndexPerformance(index_id):
    print('getIndexPerformance()')

    query = ' select t2.id,t1.name index_name, t2.index_id index_id, '\
        ' t2.p_month month, t2.p_year year,one_month, three_months,six_months,twelve_months,two_year_cagr,three_year_cagr,five_year_cagr,ten_year_cagr '\
        ' from index_performance t2, index_master t1 '\
        ' where t1.id = t2.index_id '\
        ' and t2.index_id = '+str(index_id)+' '\
        ' order by year desc, month desc, t2.id desc limit 100 ' 
    
    print('------')
    print( query)
    print('------')
    
    label_index_perf = ('id','index_name', 'index_id', 'month', 'year', 'one_month', 'three_months', 'six_months', 'twelve_months', 'two_year_cagr', 'three_year_cagr', 'five_year_cagr', 'ten_year_cagr')

    sql = text(query)
    records = db.engine.execute(sql)
    # print(records)

    tuple_list = [i for i in records]
    tuple = tuple_list[0]
    index_perf = tuple
    return tuple_list 

def getPmsDetails(pms_id):
    print('getPmsDetails()')

    query = ' select '\
            ' t1.id pms_internal_id, t1.name pms_name, stocks_min min, stocks_max max, aum ,portfolio_pe, large_cap, mid_cap, small_cap, cash, t2.name index_name '\
            ' from pms_master t1 , index_master t2'\
            ' where pms_id = '+str(pms_id) + ''\
            ' and t1.index_id = t2.id '
    
    labels = ('pms_internal_id', 'pms_name', 'min', 'max', 'aum', 'portfolio_pe', 'large_cap', 'mid_cap', 'small_cap', 'cash') 

    sql = text(query)
    records = db.engine.execute(sql)
    # print(records)

    tuple_list = [i for i in records]
    tuple = tuple_list[0]
    pms_details = tuple
    return pms_details


def getPmsStocks(pms_id):
    print('getPmsStocks()')

    query = ' select ' \
            ' t1.pct_deployed , t2.name stock_name ,t1.stock_id stock_id,t2.stock_symbol, t2.isin_code'\
            ' from pms_stock t1, stock_master t2 '\
            ' where t1.stock_id = t2.id '\
            ' and t1.pms_id ='+ str(pms_id) 
                

    sql = text(query)
    records = db.engine.execute(sql)
    # print(records)

    tuple_list = [i for i in records]
    pms_stocks = tuple_list
    # print('...........')
    # print(len(pms_stocks))
    # for tuple in pms_stocks:
    #     print(tuple)

    # print('...........')
    return pms_stocks


def getPmsSectors(pms_id):
    print('getPmsSectors()')

    query = ' select '\
            ' t1.pct_deployed , t2.name sector_name ,t1.sector_id sector_id, t2.sector_code'\
            ' from pms_sector t1, sector_master t2 '\
            ' where t1.sector_id = t2.id '\
            ' and t1.pms_id = '+str(pms_id)
                

    sql = text(query)
    records = db.engine.execute(sql)
    # print(records)

    tuple_list = [i for i in records]
    pms_sectors = tuple_list
    print('...........')
    print(len(pms_sectors))
    for tuple in pms_sectors:
        print(tuple)

    print('...........')
    return pms_sectors



def userEntitledToChange(user_id, pms_id):
    print('userEntitledToChange()')

    query = ' select count(*) count from user where id = '+ str(user_id) +''\
            ' and amc_id = (select amc_id from pms_master where pms_id = '+str(pms_id)+')'
                

    sql = text(query)
    records = db.engine.execute(sql)
    # print(records)

    tuple_list = [i for i in records]
    rec_count = tuple_list[0].count

    # print('...........')
    authorised = False
    if rec_count is None:
        # print('rec count is 0')
        authorised = False
    else:
        # print(rec_count)
        authorised = True

    return authorised


    # delete all the records from the pms_stocks table for given pms_id
def deletePmsStocks(pms_id):
    print('deletePmsStocks()')
    print("pms_id ==>", pms_id)
    # delete_query = 'delete from pms_stock where pms_id = ' + str(pms_id)
    # delete_query = 'delete from pms_stock where pms_id = ' + str(pms_id)
    query = 'delete from pms_stock where pms_id = ' + str(pms_id)
    sql = text(query)
    records = db.engine.execute(sql)
    # print(records)
    db.session.commit()

    return True


def deletePmsSectors(pms_id):
    print('deletePmsSectors()')
    print("pms_id ==>", pms_id)
    # delete_query = 'delete from pms_stock where pms_id = ' + str(pms_id)
    # delete_query = 'delete from pms_stock where pms_id = ' + str(pms_id)
    query = 'delete from pms_sector where pms_id = ' + str(pms_id)
    sql = text(query)
    records = db.engine.execute(sql)
    print(records)
    db.session.commit()

    return True

def getIndexListing():
    print('getIndexListing()')
    
    query = 'select t1.id id, t1.index_ref, t1.name index_name, t1.index_code    '\
            ' from  index_master t1  '
    

    sql = text(query)
    records = db.engine.execute(sql)
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
                            'pms_id': 'Scheme Id'
                            
                            })   

    # shifting column positions

    popped = merged_df.pop('Company Name')
    merged_df.insert(0, 'Company Name', popped)
    popped = merged_df.pop('Scheme Name')
    merged_df.insert(1, 'Scheme Name', popped)

    return merged_df


def getPMSPerfDF(month, year):
    # print('getPMSPerfDF()')
    
    # query = 'select   '\



    query = 'select *   '\
            ' from  amc_master t1 '\
            ' where amc_id > 0'

    sql = text(query)
    records = db.engine.execute(sql)
    df_amc = pd.DataFrame(records.fetchall(), columns=records.keys())
    df_amc = df_amc.drop(columns=['id','created_at'], axis=1)
    df_amc = df_amc.rename(columns={'name': 'Company Name'}) 

    query = 'select *   '\
            ' from  pms_master t1 '\
            
    sql = text(query)
    records = db.engine.execute(sql)
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

    # print(df_pms.keys())
    

    # popping the AUM column and inserting it into correct place after cash
    popped = df_pms.pop('AUM')
    df_pms.insert(10, 'AUM', popped)
    
    # print('Before Adding Category...',df_pms.keys())    
    
    
    # Adding Structure and Category column
    
    df_pms["Category"] = 3
    df_pms["Structure"] = 1    
    
    # print('After adding structure ', df_pms.keys())    
        
    # popping the Category and Structure column and inserting it into correct place after Scheme ID
    popped = df_pms.pop('Category')
    df_pms.insert(3, 'Category', popped)
        
    popped = df_pms.pop('Structure')
    df_pms.insert(4, 'Structure', popped)    
    
    # print(df_pms.keys())    
    
    
    query = 'select *   '\
            ' from  pms_performance t1  '\
            ' where p_month = '+str(month)+' '\
            ' and p_year = '+str(year)+''
    
    sql = text(query)

    # print(sql)
    records = db.engine.execute(sql)
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
                                    'si': 'Out Performance'                                   
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
    records = db.engine.execute(sql)
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
    records = db.engine.execute(sql)
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