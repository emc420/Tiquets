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
