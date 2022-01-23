import psycopg2
import pandas as pd
import math


def create_csv(csv_path):
    
    #validation of data
    
    listO = [] 
    listB = []
    for index, row in (read_excel(csv_path+'\orders.csv')).iterrows():
        dict1={}
        dict1['customer_id'] = row['customer_id']
        dict1['order_id'] = row['order_id']
        listO.append(dict1)
    for index, row in (read_excel(csv_path+'\\barcodes.csv')).iterrows():
        dict1={}
        dict1['barcode'] = row['barcode']
        dict1['order_id'] = row['order_id']
        listB.append(dict1)
     
    # generates output file that contains customer_id, order_id1, [barcode1, barcode2, ...]
    
    colate = ((pd.merge(pd.DataFrame(listO), pd.DataFrame(listB), on="order_id")).sort_values(['customer_id', 'order_id'])).reset_index()
    temp_cust = None
    temp_order = None
    dict1 = {}
    list_codes=[]
    listModified=[]
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
        list_codes.append(math.trunc(row['barcode']))
    dict1['barcode'] = list_codes
    listModified.append(dict1)    
    final_out = (pd.DataFrame(listModified)).sort_values(['customer_id'])
    final_out.to_csv('output.csv')
    
    #top 5 customers
    print('########Top 5 customers having maximum tickets#####')
    print(top5cust(final_out))
    
    #unused barcodes
    
    #db storage

def read_excel(filepath):
    df=pd.read_csv(filepath)
    return df
    
def top5cust(data_out):
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
            dict1['customer_id'] = math.trunc(row['customer_id'])
            temp_cust = row['customer_id']
        cnt = cnt+len(row['barcode'])
    return (pd.DataFrame(listModified)).nlargest(5, 'amount_of_tickets')

create_csv('data')

