import xlwings as xw

import pandas as pd





# amc_name = header.range("A1:A2").options(pd.DataFrame).value
# month = header.range("B1:B2").options(pd.DataFrame).value
# year = header.range("C1:C2").options(pd.DataFrame).value
# strategies = header.range("D1:D10").options(pd.DataFrame).value

# header_df = strategies = header.range("A1:D10").options(pd.DataFrame).value

# print(amc_name, month, year, strategies)
# print(header_df)

# writing the dataframe to a sheet
# xw.view(df)

def readHeader(wk, book_name):
    header = wk.sheets("Header")
    core_data = header.range("A1:B5").value
    # print(core_data)
    
# Using a dictionary comprehension
    header_info = {item[0]: item[1] for item in core_data if item != ['Attributes', 'Value']}
    # print(header_info)
    
    strategy_data = header.range("C2:C12").value
    # print(strategy_data)
    # removing None from it
    strategies_list = [item for item in strategy_data if item is not None]
    # print(f" total strategies= {len(strategies_list)}")
    return header_info , strategies_list
    



def readDataFromSheets(wk, book_name, strategies):
    
    amc_data = {}
    for sheet_name in strategies:
        # print(f"Strategy = {sheet_name}")
        
        # Get all sheet names in the workbook
        all_sheets = [sheet.name for sheet in wk.sheets]
        
        if sheet_name not in all_sheets:
            print(f"Error: Sheet '{sheet_name}' does not exist in workbook '{book_name}'")
            continue
        
        strategy_sheet = wk.sheets[sheet_name]
        
        # Verify we're on the correct sheet
        if strategy_sheet.name != sheet_name:
            print(f"Error: Accessed sheet '{strategy_sheet.name}' instead of '{sheet_name}'")
            continue
        
        pms_data = readPmsDataFromSheet(strategy_sheet)
        amc_data[strategy_sheet.name] = pms_data
        
    return amc_data
    

        
        
def readPmsDataFromSheet(strategy_sheet):
    
        pms_data = {}
        
        pms_alloc = extractPmsAllocData(strategy_sheet)
        pms_perf = extractPmsPerfData(strategy_sheet)
        pms_sector = extractPmsSectorData(strategy_sheet)
        pms_stock = extractPmsStockData(strategy_sheet)
        pms_nav = extractPmsNavData(strategy_sheet)
        
        pms_data['allocation'] = pms_alloc
        pms_data['pms_perf'] = pms_perf
        pms_data['pms_sector'] = pms_sector
        pms_data['pms_stock'] = pms_stock
        pms_data['pms_nav'] = pms_nav
        
        return pms_data


def extractPmsAllocData(strategy_sheet):
        data = strategy_sheet.range("A1:B9").value
        data = {item[0].strip(): item[1] for item in data}

        # print(data)
        # print("--------------------")
        return data
        
def extractPmsPerfData(strategy_sheet):
        data = strategy_sheet.range("A12:B21").value
        # data = {item[0].strip(): item[1] for item in data}

        # print(data)
        # print("--------------------")
        return data

    
def extractPmsSectorData(strategy_sheet):
        data = strategy_sheet.range("E2:F22").value
                # cleaned data
        data = [sublist for sublist in data if None not in sublist]
        # data = {item[0].strip(): item[1] for item in data}
        # Using a dictionary comprehension
        # data = {int(item[0]): (item[1], item[2]) for item in data if item[1] is not None}        

        # print(data)
        # print("--------------------")
        return data
    
def extractPmsStockData(strategy_sheet):
        data = strategy_sheet.range("I2:J22").value
        # cleaned data
        data = [sublist for sublist in data if None not in sublist]
        # data = {item[0].strip(): item[1] for item in data}
        # data = {int(item[0]): (item[1], item[2]) for item in data if item[1] is not None}          

        # print(data)
        # print("--------------------")
        return data

def extractPmsNavData(strategy_sheet):
        data = strategy_sheet.range("M2:O22").value
        
        # cleaned data
        data = [sublist for sublist in data if None not in sublist]
        
        # data = {item[0].strip(): item[1] for item in data}
        # data = {int(item[0]): (item[1], item[2]) for item in data if item[1] is not None}  

        # print(data)
        # print("--------------------")
        return data 

def parse_excel(book_name):


# book_name = 'tempdata/UIforAMCTemplate1.xlsx'
    print("starting ...")
    wk = xw.books.open(book_name)
                
    header_info , strategy_list = readHeader(wk,book_name=book_name)
    amc_data = readDataFromSheets(wk,book_name=book_name, strategies=strategy_list)

    # print(header_info)
    # print('*****')
    # print(strategy_list)
    # print('*****')
    # print(amc_data)
    wk.close()
    return header_info , strategy_list, amc_data