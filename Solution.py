import psycopg2
import pandas as pd
import math


def create_csv(csv_path):
    df_orders = read_excel(csv_path+'\orders.csv')
    df_barcodes = read_excel(csv_path+'\\barcodes.csv')
    listO = [] 
    listB = []
    for index, row in df_orders.iterrows():
        dict1={}
        take_off = {}
        land = {}
        dict1['customer_id'] = row['customer_id']
        dict1['order_id'] = row['order_id']
        listO.append(dict1)
    for index, row in df_barcodes.iterrows():
        dict1={}
        take_off = {}
        land = {}
        dict1['barcode'] = row['barcode']
        dict1['order_id'] = row['order_id']
        listB.append(dict1)
    df2 = pd.DataFrame(listO)
    df3 = pd.DataFrame(listB)
    colate = pd.merge(df2, df3, on="order_id")
    colate = colate.sort_values(['customer_id'])
    colate = colate.reset_index()
    temp_cust = None
    temp_order = None
    dict1 = {}
    list_codes=[]
    listModified=[]
    for index, row in colate.iterrows():
        if temp_cust!=row['customer_id'] and temp_order!=row['order_id']:
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
    final_out = pd.DataFrame(listModified)   
    final_out = final_out.sort_values(['customer_id'])
    final_out.to_csv('output.csv')

def read_excel(filepath):
    df=pd.read_csv(filepath)
    return df
    
    

create_csv('data')

