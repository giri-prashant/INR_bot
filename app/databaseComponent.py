
import pandas as pd
import sqlite3
from datetime import datetime
import Constants
from qrlib.QRUtils import  display
from qrlib.QRComponent import QRComponent 
import oracledb
current_date = datetime.now().strftime('%Y-%m-%d')

class DBComponent(QRComponent):
    def __init__(self):
        self.conn = None
        self.cur = None
        self.table_name = Constants.db_table_name
        
        
    def connect(self):
        self.conn = sqlite3.connect(Constants.DB_PATH)
        self.cur = self.conn.cursor()
        display("databased connected !!!! ")
    
    def close_connection(self):
        self.cur.close()
        self.conn.close()
        
    def create_table(self):
        self.con = sqlite3.connect(Constants.DB_PATH)
        self.cur = self.con.cursor()

        query = f'''
            CREATE TABLE IF NOT EXISTS {self.table_name} (
                filename VARCHAR(55),
                last_inserted_date VARCHAR(55)
            )
        '''

        self.cur.execute(query)
        self.con.commit()
        self.con.close()

        display('Successfully created table excel_db with columns filename and last_inserted_date')

    def create_trigger(self):
        self.con = sqlite3.connect(Constants.DB_PATH)
        self.cur = self.con.cursor()
        query = f"""
        CREATE TRIGGER IF NOT EXISTS update_timestamp AFTER UPDATE ON  {self.table_name} FOR EACH ROW
        BEGIN UPDATE {self.table_name} SET updated_date = (datetime('now', 'localtime')) WHERE transId = NEW.transId; END;"""
        self.con.row_factory = sqlite3.Row
        self.con.execute(query)
        self.con.commit()
        self.con.close()


    def insert_excel_data(self, filename, last_inserted_date):
        self.con = sqlite3.connect(Constants.DB_PATH)
        self.cur = self.con.cursor()
        
        # Construct the SQL query
        query = '''
            INSERT INTO excel_db (filename, last_inserted_date)
            VALUES (?, ?)
        '''
        
        # Execute the query with the provided filename and last_inserted_date
        self.cur.execute(query, (filename, last_inserted_date))
        self.con.commit()
        self.con.close()
        display('Successfully inserted data into the database')

    def get_most_recent_date(self):
        self.con = sqlite3.connect(Constants.DB_PATH)
        self.cur = self.con.cursor()
        query = f'''
            SELECT date_column_name FROM {self.table_name}
            ORDER BY date_column_name DESC
            LIMIT 1;
        '''
        self.cur.execute(query)
        most_recent_date = self.cur.fetchone()
        
        if most_recent_date:
            display(f'Most recent date: {most_recent_date[0]}')
            return most_recent_date[0]
        else:
            return None
        
    def get_summary_report(self,date):
        self.con = sqlite3.connect(Constants.DB_PATH)
        self.cur = self.con.cursor()
        query = f'''
             SELECT * FROM {self.table_name}
            WHERE pdf_file_status = 'inserted'  AND [report_date]= '{date}';
        '''
        self.con.row_factory = sqlite3.Row
        data = self.con.execute(query).fetchall()
        if data:
            temp_value = [{str(key): item[key] for key in item.keys()} for item in data]
            display('get the data for posting sucess runitem')
            df = pd.DataFrame(temp_value)
            return df
        else:
            return []
        
    def get_dollar_amount_for_prepaidcard(self,Ref_value):
        display("-- from db ")
        query = f" select  BILL_AMT from sblpsd.tbl_daily_transaction where Ref_NUM = '{Ref_value}'  " 
        user = 'fcjglhist'
        password = 'fcjglhist'
        host_name = '10.60.100.1'
        port = '1521'
        service = 'SBLDB'
        try:
            dsn_tns = oracledb.makedsn(host_name, port, service_name=service) 
            conn = oracledb.connect(user=user,  password=password, dsn=dsn_tns )
            cursor = conn.cursor()
            cursor.execute(query)
            data = cursor.fetchone()
            display(data[0])
            conn.close()
            return data[0]
        except Exception as e:
            print(f'error occured { e }')
        


# select  * from sblpsd.tbl_daily_transaction where Ref_NUM = '413404364928' and TRANSACTION_DATE ='13-may-2024'
