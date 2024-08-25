import math
import pandas as pd
from io import BytesIO
import numpy as np

# https://xlsxwriter.readthedocs.io/example_pandas_column_formats.html
# Create a Pandas dataframe from some data.
df = pd.DataFrame(
    {
        "Numbers": ['A', 'B' , 'C' ,'D' ,'E','F','G'],
        "Percentage": [0.1, 0.2, 0.33, 0.25, 0.5, 0.75, 0.45],
        "Numbers": [1010, 2020, 3030, 2020, 1515, 3030, 4545],
        "Percentage": [0.1, 0.2, 0.33, 0.25, 0.5, 0.75, 0.45],
    }
)

def write_report(df,month, year):

    # divide the columns by 100 which needs to be formatted to percentage in Excel
    df[['large_cap', 'mid_cap', 'small_cap']] = df[['large_cap', 'mid_cap', 'small_cap']].div(100)

    # Create a Pandas Excel writer using XlsxWriter as the engine.
    writer = pd.ExcelWriter("PMSReport"+ str(year)+"_"+str(month)+".xlsx", engine="xlsxwriter")

    # Convert the dataframe to an XlsxWriter Excel object.
    df.to_excel(writer, sheet_name="Sheet1")

    # Get the xlsxwriter workbook and worksheet objects.
    workbook = writer.book
    worksheet = writer.sheets["Sheet1"]

    # Add some cell formats.
    number_format = workbook.add_format({"num_format": "#,##0.00"})
    percent_format = workbook.add_format({"num_format": "0%"})

    # Note: It isn't possible to format any cells that already have a format such
    # as the index or headers or any cells that contain dates or datetimes.

    # Set the column width and format.
    # worksheet.set_column(1, 1, 18, number_format)

    # Set the format but not the column width.
    # worksheet.set_column(2, 2, None, percent_format)
    worksheet.set_column('K:N', None, percent_format)

    # Close the Pandas Excel writer and output the Excel file.
    writer.close()


def write_Excel_report(df):

    excel_file = BytesIO()

    # divide the columns by 100 which needs to be formatted to percentage in Excel
    df[['Large', 'Mid', 'Small', 'cash']] = df[['Large', 'Mid', 'Small', 'cash']].div(100)

    df[['1m', '3m','6m','1y','2y','3y','5y','10 yrs','SI']] = df[['1m', '3m','6m','1y','2y','3y','5y','10 yrs','SI']].div(100)

    df[['1 Month Benchmark', '3 Month Benchmark','6 Month Benchmark','1 Year Benchmark','2 Year Benchmark','3 Year Benchmark','5 Year Benchmark','10 Year Benchmark']] = df[['1 Month Benchmark', '3 Month Benchmark','6 Month Benchmark','1 Year Benchmark','2 Year Benchmark','3 Year Benchmark','5 Year Benchmark','10 Year Benchmark']].div(100)



    with pd.ExcelWriter(excel_file, engine='xlsxwriter') as writer:
    # with pd.ExcelWriter(excel_file, engine='xlsxwriter', options={'nan_inf_to_errors': True}) as writer:    
 
        # Add the XlsxWriter workbook object
        workbook = writer.book
        
        # Replace NaN and INF values with strings
        # df.replace([np.nan, np.inf, -np.inf], ['NaN', 'INF', '-INF'], inplace=True)
     
        
        df.to_excel(writer, sheet_name='Sheet_1', index=False)
        worksheet1 = writer.sheets['Sheet_1']

        # Adding formatters:
        format_integer = writer.book.add_format({"num_format": "#,##0"})        
        format_decimal = writer.book.add_format({"num_format": "#,##0.00"})
        format_percent = writer.book.add_format({'num_format': '0.00%'})

        # Add formats
        header_format = writer.book.add_format({'bg_color': 'yellow', 'border': 1})
        center_format = writer.book.add_format({'align': 'center'})

        # Apply header format and center alignment
        for col_num, value in enumerate(df.columns.values):
            worksheet1.write(0, col_num, value, header_format)
            worksheet1.set_column(col_num, col_num, None, center_format)

   

        # Apply center alignment
        for col_num in range(len(df.columns)):
            worksheet1.set_column(col_num, col_num, None, center_format)       

        # Increase width of first two columns
        worksheet1.set_column('A:B', 15)  # Increase width to 15 

        # Sheet 2 with default format
        df.to_excel(writer, sheet_name='Sheet_2', index=False)

        # Apply Formatting columns for number
        worksheet1.set_column('F:F', None, format_integer)

        # Apply Formatting columns for percentage
        worksheet1.set_column('I:L', None, format_percent)
        # Apply Formatting columns for number
        worksheet1.set_column('M:M', None, format_decimal)    
        # Apply Formatting columns for percentage                
        worksheet1.set_column('N:V', None, format_percent)      
        # Apply Formatting columns for number
        worksheet1.set_column('W:W', None, format_decimal)      
        # Apply Formatting columns for percentage              
        worksheet1.set_column('X:AF', None, format_percent)      

        # Add autofilter to all columns
        # worksheet1.autofilter(0, 0, df.shape[0], df.shape[1] - 1)
  
        # # Add sorting options to each column
        # for col_num, value in enumerate(df.columns.values):
        #     for row_num, val in enumerate(df[value], start=1):
        #         print('OUTER -', row_num, col_num, val, type(val))
        #         # if isinstance(val, float) and math.isnan(val): 
        #         # print(val)
        #         if type(val) == type('str'):
        #             print(' STRING FOUND  INSTANCE ==>',row_num, col_num, val)
        #             # print( 'float ==> math value ==> ' , math.isnan(val))
        #             # if math.isnan(val):
        #             worksheet1.write(row_num, col_num, 0)
        #         else:
        #             worksheet1.write(row_num, col_num, val)

        # Apply conditional formatting to hide NaN values
        # nan_format = workbook.add_format({'font_color': '#FFFFFF'})  # Set font color same as background to hide text
        # worksheet1.conditional_format(1, 0, df.shape[0], df.shape[1] - 1, {'type': 'cell', 'criteria': '==', 'value': 'NA',
        #                                                                 'format': nan_format})


    # Move to the beginning of the BytesIO buffer
    excel_file.seek(0)

    return excel_file
