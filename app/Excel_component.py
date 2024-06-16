
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
    
