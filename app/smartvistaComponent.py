
from glob import glob
import time
import traceback
from datetime import datetime
from selenium import webdriver
from datetime import datetime,timedelta
import os
# from robot.libraries.BuiltIn import BuiltIn
from RPA.Browser.Selenium import Selenium, FirefoxOptions
from qrlib.QRDecorators import run_item
from qrlib.QRUtils import get_secret, display

from qrlib.QRComponent import QRComponent
# from app.Utils import wait_and_click,wait_and_input_text
import Constants
from qrlib.QREnv import QREnv
# from app.Email import EmailComponent
import pandas as pd
import numpy as np
from Utils import delete_files_in_folder
# display = BuiltIn().log_to_console
class SmartVistaComponent(QRComponent):
    def __init__(self):
        super().__init__()
        self.browser = Selenium()
        self.username = ''
        self.password = ''
        self.url = ''

    def load_smartvista_vault(self):
        self.smartvista_vault = QREnv.VAULTS['smartvista']
        self.username = self.smartvista_vault['username']
        self.password = self.smartvista_vault['password']
        self.url = self.smartvista_vault['url']

    def open_smartvista(self):
        logger = self.run_item.logger
        # BROWSER_PATH = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
# DRIVER_PATH = "C:\\\\Users\\\\Dell\\\\AppData\\\\Local\\\\robocorp\\\\webdrivers\\\\.wdm\\\\drivers\\\\IEDriverServer\\\\win64\\\\4.14.0\\\\IEDriverServer.exe"
# chrome_options = webdriver.ChromeOptions()
        ie_options=webdriver.IeOptions()
        ie_options.attach_to_edge_chrome=True
        ie_options.ignore_zoom_level=True
        # ie_options.edge_executable_path=BROWSER_PATH
        ie_options.native_events = True
        ie_options.ignore_protected_mode_settings=True
        ie_options.require_window_focus=False
        ie_options.add_additional_option("ie.edgechromium", True)

        edge_options = webdriver.EdgeOptions()
        edge_options.use_chromium = True
        edge_options.add_argument("ie-mode-test")
        self.browser.set_download_directory(Constants.download_path)

        # self.browser.open_available_browser(url=None, browser_selection='edge') #, download=True, options=ie_options)
        self.browser.open_available_browser(url=self.url, browser_selection='edge') #, download=True, options=ie_options)
        display("opened Browser")
        self.browser.maximize_browser_window()
        display("maximized Browser")
        logger.info("Browser opened")

        time.sleep(3)
        self.wait_and_click('//button[@id="details-button"]')
        self.wait_and_click('//*[@id="proceed-link"]')

        # options = FirefoxOptions
        # options.set_preference("browser.download.folderList",2)
        # options.set_preference("browser.download.manager.showWhenStarting",False)
        # options.set_preference("browser.download.dir",Constants.DOWNLOADDIR)
        # options.set_preference("browser.helperApps.neverAsk.saveToDisk","application/x-gzip")
        # self.browser.open_available_browser(
        #     url=self.url,
        #     browser='firefox',
        #     options=options
        # )
        # self.browser.maximize_browser_window()
        # self.selenium.set_window_size(1920, 1080)
        logger.info('SmartVista browser opened successfully')
        display('SmartVista browser opened successfully')

    def login_smartvista(self):
        logger = self.run_item.logger
        logger.info(f'logging in to smart vista  ')
        self.browser.wait_until_element_is_visible('//div[@class="login-div"]', timeout=Constants.TIMEOUT)
        self.browser.wait_until_element_is_visible('//input[@id="LoginForm:Login"]', timeout=Constants.TIMEOUT)
        self.browser.input_text('//input[@id="LoginForm:Login"]', text=self.username, clear=True)
        self.browser.wait_until_element_is_visible('//input[@id="LoginForm:Password"]', timeout=Constants.TIMEOUT)
        self.browser.input_password('//input[@id="LoginForm:Password"]', password=self.password, clear=True)
        self.browser.wait_until_element_is_visible('//input[@id="LoginForm:submit"]', timeout=Constants.TIMEOUT)
        self.browser.click_element('//input[@id="LoginForm:submit"]')
        self.browser.wait_until_element_is_visible("//div[@class='pageName']",timeout=Constants.TIMEOUT)

        logger.info(f'logged in to smart vista ')
        display("logged in to smart vista ")


    def logout_smartvista(self):
        logger = self.run_item.logger
        display("logout successfully")
        try:
            LOGOUT_PATH = "//a[@id = 'userBar:logoutLink']"
            self.browser.wait_until_element_is_visible(LOGOUT_PATH,Constants.TIMEOUT)
            # self.browser.click_element(LOGOUT_PATH)
            self.browser.execute_javascript('document.getElementById("userBar:logoutLink").click()')
        except Exception as e:
            logger.error(traceback.format_exc())
        

    def download_excelfile(self):
        logger = self.run_item.logger
        logger.info(f'downloading csv file ------------')
        delete_files_in_folder(logger,Constants.download_path)
        delete_files_in_folder(logger,Constants.all_files_path)
        display(f'downloading csv file ------------')
        # today_date = datetime.now()
        
        xpath = {
            'report':'//div[@id="headerMenuForm:reports"]',
            'report_sub': '//div[@id="headerMenuForm:rep_frozenQueries"]',
            'other_reports': '//img[@id="commandForm:freeTree:1:50::j_id91:handle:img:collapsed"]',
            'sidhartha_report':"//img[@id='commandForm:freeTree:1:50:337::j_id91:handle:img:collapsed']",
            'merchant_settlement': '//td[@id="commandForm:freeTree:1:50:337:344::j_id91:text"]',
            'execute':'//input[@id="commandForm:executeJ"]',
            'select_filetype':'//select[@name="mp2Form:j_id206"]', #value="XML"
            'start_date':'//input[@id="mp2Form:j_id154:2:fieldDInputDate"]',
            'end_date':'//input[@id="mp2Form:j_id154:3:fieldDInputDate"]',
            # 'end_date':'id="mp2Form:j_id154:3:fieldDInputDate"', #2431
            'export':'//input[@id="mp2Form:export"]', #0483
            }
        try:
            self.wait_and_click(xpath['report'])
            self.wait_and_click(xpath['report_sub'])
            self.wait_and_click(xpath['other_reports'])
            self.wait_and_click(xpath['sidhartha_report'])
            self.wait_and_click(xpath['merchant_settlement'])
            self.wait_and_click(xpath['execute'])

            self.browser.wait_until_element_is_visible(xpath['select_filetype'])
            self.browser.select_from_list_by_value(xpath['select_filetype'],"CSV")

            # start_date = datetime.now().strftime("%d.%m.%Y")
            start_date =Constants.thirty_days_ago_formatted
            end_date =Constants.thirty_days_ago_formatted
            # self.browser.input_text(xpath['start_date'], text=start_date, clear=True)
            self.browser.set_element_attribute(xpath['start_date'],attribute='value',value=start_date)
            # self.browser.input_text(xpath['end_date'], text=end_date, clear=True)
            self.browser.set_element_attribute(xpath['end_date'],attribute='value',value=end_date)

            # self.wait_and_click(xpath['start_date'])
            # self.wait_and_click(xpath['end_date'])
            self.wait_and_click(xpath['export'])
            self.check_file_downloaded_or_not('.csv')

            logger.info(f'Merchant Report in CSV file format  downloaded ')
            display(f'Merchant Report in CSV file format  downloaded ')

        except Exception as e:
            logger.error(traceback.format_exc())
            logger.info(f'Merchant Report in CSV file format  not downloaded ')
            display(f'Merchant Report in CSV file format not  downloaded ')
    

        
    def check_file_downloaded_or_not(self,file_extension):
        logger = self.run_item.logger

        file_path = Constants.download_path
        start_time = time.time()
        timeout_second = 700
        while (time.time() - start_time) < timeout_second: 
            # Use glob to check for files with the .xlsx extension
            files = glob(os.path.join(file_path, f"*{file_extension}"))
            # If files list is not empty, it means at least one .xlsx file exists
            if files:
                logger.info(f'downloaded files == {files}')
                break
            time.sleep(1)
        else:
            raise Exception(f"Time out while downloading file")

    def wait_and_click(self, xpath):
        logger = self.run_item.logger if hasattr(self, 'run_item') else self.logger
        try:
            self.browser.wait_until_element_is_visible(xpath, timeout=Constants.TIMEOUT)
            self.browser.click_element(xpath)
        except Exception as e:
            logger.error(f'error processing xpath: {xpath}')
            logger.error(e)
            raise e

    def close_browser(self):
        self.selenium.close_browser()