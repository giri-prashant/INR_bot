
from datetime import datetime
import requests
from openpyxl import load_workbook
from openpyxl.styles import Alignment

from openpyxl.worksheet.cell_range import CellRange

from RPA.Browser.Selenium import Selenium, FirefoxOptions
from qrlib.QRDecorators import run_item
from qrlib.QRRunItem import QRRunItem
from qrlib.QRUtils import get_secret, display

from qrlib.QRComponent import QRComponent
# from app.Utils import wait_and_click,wait_and_input_text
import Constants
from qrlib.QREnv import QREnv
# from app.Email import EmailComponent
import pandas as pd
import numpy as np
from databaseComponent import DBComponent


class ExcelComponent(QRComponent):
    def __init__(self):
        super().__init__()
        
    def read_excel_file(self,file_path):       
        df = pd.read_excel(Constants.file_path)
        filtered_df = df[(df['CARD_NUMBER'].str.startswith(('443832', '463726'))) & (df['CURR_CODE'] == 356)]   
        actual_transactions = ['5TCN05','5TCN07']
        reversal_transactions = ['5TCN06','5TCN25','5TCN27']

        df = pd.read_excel(file_path,dtype=str)
        filtered_df = df[(df['CARD_NUMBER'].str.startswith(('443832', '463726')))]
        filtered_df1 = filtered_df[(filtered_df['TXN_CURR'].str.startswith('356'))]
        actual_txn_df = filtered_df[filtered_df['TC'].isin(actual_transactions)].copy()
        reversal_txn_df = filtered_df[~filtered_df['TC'].isin(actual_transactions)].copy()
        # print(len(actual_txn_df))

        for index, row_actual in actual_txn_df.iterrows():
            for index_rev, row_reversal in reversal_txn_df.iterrows():
                if row_actual['AUTH_ID'] == row_reversal['AUTH_ID']:
                    if row_actual['TXN_AMT'] == row_reversal['TXN_AMT']:
                        # Remove from actual_txn_df
                        actual_txn_df.drop(index, inplace=True)
                        break
        
                
            total_amt = sum(float(i) * 0.0015 for i in actual_txn_df['TXN_AMT'].tolist())
            return total_amt           