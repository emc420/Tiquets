import pandas as pd
import math, sys
from database import data_model as db 

import logging
logging.basicConfig(filename='errorLogs\\app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')

def main(): 

    try:
        listO = [] 
        listB = []
        for index, row in (read_csv('data\orders.csv')).iterrows():
            listO.append({'customer_id':str(row['customer_id']), 'order_id':str(row['order_id']) })
        for index, row in (read_csv('data\\barcodes.csv')).iterrows():
            listB.append({'barcode':None if math.isnan(row['barcode']) else str(math.trunc(row['barcode'])), 'order_id':None if math.isnan(row['order_id']) else str(math.trunc(row['order_id'])) })
         
        #validation of data
        barcodes = validate_duplicate_barcodes(no_orders_without_barcodes(pd.DataFrame(listB)))
        orders = pd.DataFrame(listO)
        colate = ((pd.merge(barcodes, orders, on="order_id")).sort_values(['customer_id', 'order_id'])).reset_index()
        temp_cust = None
        temp_order = None
        dict1 = {}
        list_codes=[]
        listModified=[]
        # generates output file that contains customer_id, order_id1, [barcode1, barcode2, ...]
        
        for index, row in colate.iterrows():
            if temp_cust!=row['customer_id'] or temp_order!=row['order_id']:
                if index!=0:
                    dict1['barcode'] = list_codes
                    listModified.append(dict1)
                dict1={}
                list_codes =[]
                dict1['customer_id'] = row['customer_id']
                dict1['order_id'] = row['order_id']
                temp_cust = row['customer_id']
                temp_order = row['order_id']
            list_codes.append(row['barcode'])
        dict1['barcode'] = list_codes
        listModified.append(dict1)    
        final_out = (pd.DataFrame(listModified)).sort_values(['customer_id'])
        final_out.to_csv('output.csv')
        
        #top 5 customers
        print('########Top 5 customers having maximum tickets#####')
        print(top5cust(final_out))
        
        #unused barcodes
        
        print('######Unused Barcodes######')
        for index, row in barcodes.iterrows():
            if row['order_id'] is None:
                print(row['barcode'])
        
        #db storage
        
        #db.insert_into_tables(orders, barcodes)
    
    except Exception as err:
        logging.error('Error Description: ', err)

def read_csv(filepath):
    try:
        df=pd.read_csv(filepath)
        return df
    except Exception as err:
        raise Exception('Error Occured while reading input :'+str(filepath), err)
    
def top5cust(data_out):
    try:
        temp_cust = None
        dict1={}
        listModified=[]
        cnt = 0
        for index, row in data_out.iterrows():
            if temp_cust!=row['customer_id']:
                if temp_cust is not None:
                    dict1['amount_of_tickets'] = cnt
                    listModified.append(dict1)
                dict1={}
                list_codes =[] 
                cnt = 0
                dict1['customer_id'] = row['customer_id']
                temp_cust = row['customer_id']
            cnt = cnt+len(row['barcode'])
        return (pd.DataFrame(listModified)).nlargest(5, 'amount_of_tickets')
    except Exception as err:
        raise Exception('Error Occured while fetching top 5 customers :', err)
    
def validate_duplicate_barcodes(barcodes):
    try:
        logging.error('#######Duplicate Barcodes#####')
        logging.error(barcodes[barcodes.duplicated(subset="barcode", keep='first')]['barcode'])
        barcodes.drop_duplicates(subset ="barcode", inplace = True)
        return barcodes
    except Exception as err:
        raise Exception('Error Occured while valdating dulplicate barcodes :', err)

def no_orders_without_barcodes(barcodes):
    try:
        for index, row in barcodes.iterrows():
            if row['order_id'] is not None and row['barcode'] is None:
                logging.error('####orders without barcodes######')
                logging.error(row['order_id'])
                barcodes.drop(index, inplace=True)
        return barcodes
    except Exception as err:
        raise Exception('Error Occured while valdating orders without barcodes :', err)


if __name__ == "__main__":
    main()
    

