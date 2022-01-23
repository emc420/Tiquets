from sqlalchemy import create_engine

db = create_engine('postgresql://postgres:postgres@localhost:5432/Tiquets')

def create_table():
    try:
        db.execute("CREATE TABLE IF NOT EXISTS orders (order_id text PRIMARY KEY, customer_id text)")  
        db.execute("CREATE TABLE IF NOT EXISTS barcodes (order_id text, barcode text, FOREIGN KEY (order_id) REFERENCES orders (order_id))") 
    except Exception as err:
        raise Exception('Error Occured while creating table in db :', err)    
    
def insert_into_tables(orders, barcodes):
    try:
        create_table()
        orders.to_sql('orders', db, if_exists='append', index=False)
        barcodes.to_sql('barcodes', db, if_exists='append', index=False)
    except Exception as err:
        raise Exception('Error Occured while insering into tables :', err)    

def fetch_top_5():
    try:
        result_set = db.execute("SELECT customer_id, COUNT(*) as amount_of_tickets FROM orders, barcodes where orders.order_id=barcodes.order_id GROUP BY customer_id ORDER BY amount_of_tickets DESC LIMIT 5")
        print('customer_id \t'+'amount_of_tickets')
        for r in result_set:  
            print(str(r['customer_id'])+'\t\t'+str(r['amount_of_tickets']))
    except Exception as err:
        raise Exception('Error Occured while fetching top 5 customers from db :', err)    
        

def fetch_unused_barcodes():
    try:
        result_set = db.execute("SELECT barcode FROM barcodes where order_id IS NULL")
        print('Unused_Barcodes')
        for r in result_set:  
            print(r['barcode'])
    except Exception as err:
        raise Exception('Error Occured while fetching unused barcodes from db :', err) 
        
        
def fetch_output():
    try:
        result_set = db.execute("SELECT customer_id, orders.order_id, STRING_AGG(barcode, ',') FROM orders, barcodes where orders.order_id=barcodes.order_id GROUP BY customer_id, orders.order_id ORDER BY customer_id, orders.order_id")
        print('customer_id \t'+'order_id \t'+ 'barcodes')
        for r in result_set:  
            print(str(r[0])+'\t\t'+str(r[1])+'\t\t'+str(r[2]))
    except Exception as err:
        raise Exception('Error Occured while fetching output from db :', err) 
        