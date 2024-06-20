import re
import time
import requests
from selenium import webdriver
from RPA.Desktop import Desktop
from RPA.Browser.Selenium import Selenium
from qrlib.QREnv import QREnv
from qrlib.QRComponent import QRComponent 
from qrlib.QRUtils import get_secret, display
import Constants
from datetime import datetime

BROWSER_PATH = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
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

class finaclecomponent(QRComponent):
    def __init__(self):
        super().__init__()
        self.browser= Selenium()

        


    def open_finacle(self):
        url = QREnv.VAULTS["finacle_entry"]["url"]
        logger = self.run_item.logger if hasattr(self, 'run_item') else self.logger
        try:
            logger.info(f"Opening Browser..")
            display("Opening Browser")
            # self.browser.open_browser(url=self.url, browser='ie', executable_path=DRIVER_PATH, options=ie_options)
            self.browser.open_available_browser(url=url, browser_selection='edge') #, download=True, options=ie_options)
            display("opened Browser")
            self.browser.maximize_browser_window()
            display("maximized Browser")
            logger.info("Browser opened")

        except Exception as e:
            display(f"Error: {e}")
            logger.error(f'error browser opening process')
            logger.error(f'{e}')

    def login(self):
        finacle_entry_username = QREnv.VAULTS["finacle_entry"]["username"]
        finacle_entry_password = QREnv.VAULTS['finacle_entry']['password']
        logger = self.run_item.logger if hasattr(self, 'run_item') else self.logger
        try:
            xpath= {
            'login_frame':"//iframe[@name='loginFrame']",
            'username': '//input[@id="usertxt"]',
            'password': '//input[@id="passtxt"]',
            'login': '//input[@id="Submit"]',
            # 'accept':'//input[@value="Accept"]'
            }
            logger.info(f"logging in..")
            self.wait_and_select_frame(xpath['login_frame'])
            self.browser.wait_until_element_is_visible(locator=xpath['username'],timeout=Constants.TIMEOUT)
            self.browser.input_text(locator=xpath['username'], text=finacle_entry_username)
            self.browser.input_password(xpath['password'], finacle_entry_password)
            
            self.browser.wait_until_element_is_visible(xpath['login'])
            self.wait_and_click(xpath['login'])
            logger.info(f'logged in')
            display("logged in  ......................")

        except Exception as e:
            logger.error(f'error logging')
            logger.error(f'{e}')
            
    def transfer_trans_value(self,amount):
        logger = self.run_item.logger
        xpath = {
            'transaction_type': '//select[@id="tranTypeSubType"]', 
            'function_type' : '//select[@id="funcCode"]',
            'click_go' : '//input[@id="Go"]'
        }
        
        logger.info(f"selecting transaction ..")    
        self.browser.select_from_list_by_value(xpath['function_type'],value="A")
        self.browser.select_from_list_by_value(xpath['transaction_type'],value="T/BI")
        self.wait_and_click(xpath['click_go'])
        self.post_amount_in_cbs(dr_cr="cr",amount=amount)
        self.wait_and_click(xpath['next'])
        self.post_amount_in_cbs(dr_cr="dr",amount=amount)
        self.wait_and_click(xpath['save'])

    def post_amount_in_cbs(self,dr_cr,amount):
        Date_format =Constants.NARR_DATE
        narration = f"INR FEE {Date_format}"
        
        xpath = {
            'click_credit': '//input[@id="pTranType"][2]',
            'click_debit': '//input[@id="pTranType"][1]',
            'acc_id': '//input[@id="acctId"]',
            'amount_click': '//input[@id="refAmt"]',
            'next' : '//img[@id="partTranDetail_NextRec"]',
            'save': '//input[@id="Save"]',
            'transaction_desc': '//input[@id="tranParticular"]'
        }
        if(dr_cr == 'cr'):
            self.wait_and_click(xpath['click_credit'])
        else:
            self.wait_and_click(xpath['click_debit'])
            self.browser.input_text(xpath['acc_id'],)
            self.browser.input_text(xpath['amount_click'],amount)
            self.browser.input_text(xpath['transaction_desc'],narration)
        
        
        

    def upload_batch(self):
        display('inside search upload')
        logger = self.run_item.logger if hasattr(self, 'run_item') else self.logger
        xpath= {
            'login_frame':"//iframe[@name='loginFrame']",
            'coreframe_frame':"//iframe[@name='CoreServer']",
            'finw_frame':"//iframe[@id='FINW']",
            'report_to':'//input[@id="report_to"]',
            'radio_action':'//input[@id="fire_bfti_flg"][1]',
            'radio_file_loc':'//input[@id="upload_file_location"][2]',
            'transaction_subtype':'//select[@id="tran_sub_type"]', #value="T|BI"
            'submit':'//div[@class="ctable"]/input[@value="Submit"]',
            'choose_file':'//input[@id="fileField"]',
            'go':'//input[@id="Continue"]'
            }
        logger.info(f"uploading  batch file ..")
        self.browser.unselect_frame()

        self.wait_and_select_frame(xpath['login_frame'])
        self.wait_and_select_frame(xpath['coreframe_frame'])
        self.wait_and_select_frame(xpath['finw_frame'])
        self.browser.input_text(locator=xpath['report_to'], text='Rpa1')
        self.browser.select_from_list_by_value(xpath['transaction_subtype'],"T|BI")
        self.wait_and_click(xpath['radio_action'])
        self.wait_and_click(xpath['radio_file_loc'])
        time.sleep(3)
        self.wait_and_click(xpath['submit'])
        time.sleep(3)
        self.browser.choose_file(xpath['choose_file'], Constants.batch_text_file)
        self.wait_and_click(xpath['go'])

    def check_batch_upload(self,value):
        time.sleep(15)
        logger = self.run_item.logger if hasattr(self, 'run_item') else self.logger
        try:
            xpath={
                # 'frame_path':'//div[@id="SSODiv"]/iframe[@name="loginFrame"]',
                'menu_selector_path':'//div[@id="widget_menuSelect"]',
                'menu_input_path':'//input[@id="menuSelect"]',
                'menu_SearchBtn_path':'//button[@id="menuSearcherGo"]',
                'login_frame':"//iframe[@name='loginFrame']",
                'coreframe_frame':"//iframe[@name='CoreServer']",
                'finw_frame':"//iframe[@id='FINW']",
                'go':'//input[@id="Go"]',
                'check_sucess':'//input[@id="chkselFlg1"]',
                'print_screen':'//input[@id="DesktopPrint"]',
                'dataframe_iframe':'//iframe[@id="dataframe"]',
                'get_text': '//span[@dir="LTR"]/pre'
            }
            self.browser.unselect_frame()
            self.wait_and_select_frame(xpath['login_frame'])
            self.wait_and_click(xpath['menu_selector_path'])
            time.sleep(1)
            self.wait_and_input(xpath['menu_input_path'],'hpr')
            time.sleep(1)
            self.wait_and_click(xpath['menu_SearchBtn_path'])
            time.sleep(1)

            logger.info(f"checking if  batch file is uploaded or not ..")
            self.browser.unselect_frame()
            self.wait_and_select_frame(xpath['login_frame'])
            self.wait_and_select_frame(xpath['coreframe_frame'])
            self.wait_and_select_frame(xpath['finw_frame'])
            self.wait_and_click(xpath['go'])
            time.sleep(5)

            self.browser.unselect_frame()
            self.wait_and_select_frame(xpath['login_frame'])
            self.wait_and_select_frame(xpath['coreframe_frame'])
            self.wait_and_select_frame(xpath['finw_frame'])
            # elem = self.browser.find_element()
            self.wait_and_click(f'//table[@id="HPR_table"]//input[@id="chkselFlg{value}"]')
            display(f'clicking xpath ===== //table[@id="HPR_table"]//input[@id="chkselFlg{value}"]')
            time.sleep(2)
            self.wait_and_click(xpath['print_screen'])

            time.sleep(5)
            self.browser.unselect_frame()
            self.wait_and_select_frame(xpath['login_frame'])
            self.wait_and_select_frame(xpath['coreframe_frame'])
            self.wait_and_select_frame(xpath['finw_frame'])
            self.wait_and_select_frame(xpath['dataframe_iframe'])
            pre_element = self.browser.find_element(xpath['get_text'])
            pre_text = pre_element.text
            display(pre_text)

            if "Tran Id" in pre_text:
                tran_id_match = re.search(r'Tran Id\s*:\s*(\w+)', pre_text)
                
                if tran_id_match:
                    tran_id = tran_id_match.group(1).strip()
                    display("Tran Id:", tran_id)
                    logger.info(f"Trancsacaton Id found {tran_id}")
                    return True
                else:
                    display("Tran Id not found")
                    return False
            try:
                alert=self.browser.handle_alert()
                logger.info(f"alert: {alert} accepted")
            except:
                logger.info("No Alert")
                
            logger.info("batch file sucessfully uploaded")
        except Exception as e:
            logger.error("Error in batch file ")
            logger.error(f"ERROR: {e}")





    def navigate_to_hxfer(self):
        logger = self.run_item.logger if hasattr(self, 'run_item') else self.logger
        try:
            xpath={
                'frame_path':'//*[@id="SSODiv"]/iframe[@name="loginFrame"]',
                'menu_selector_path':'//div[@id="widget_menuSelect"]',
                'menu_input_path':'//input[@id="menuSelect"]',
                'menu_SearchBtn_path':'//button[@id="menuSearcherGo"]',
                
            }
            
            self.browser.unselect_frame()
            self.wait_and_select_frame(xpath['frame_path'])
            self.wait_and_click(xpath['menu_selector_path'])
            time.sleep(1)
            self.wait_and_input(xpath['menu_input_path'],'hxfer')
            time.sleep(1)
            # self.browser.press_keys(xpath['menu_selector_path'],"enter")
            self.wait_and_click(xpath['menu_SearchBtn_path'])
            time.sleep(1)
            try:
                alert=self.browser.handle_alert()
                logger.info(f"alert: {alert} accepted")
            except:
                logger.info("No Alert")
                
            logger.info("Navigated to HICMTO")
        except Exception as e:
            logger.error("Error in Navigation to HICMTO")
            logger.error(f"ERROR: {e}")
    
    
    def open_mis_check_approval(self):
        logger = self.run_item.logger if hasattr(self, 'run_item') else self.logger
        url = 'https://10.60.103.3:44444/xmlpserver/Finacle+Reports/Common+Reports/Daily+Transaction+Report/Daily+Transaction+Report.xdo'
        username = QREnv.VAULTS["sbl_mis"]["username"]
        password = QREnv.VAULTS['sbl_mis']['password']
        xpath = {
            'username':'//input[@id="id"]',
            'password': '//input[@id="passwd"]',
            'signin': '//input[@value="Sign In"]',
            'input_field':"//input[@id='PUSERID']",
            'view': '//form[@id="xdoRptForm"]/table[3]/tbody/tr/td[1]/button[1]',

            'frame':'//iframe[@id="xdo-report-body"]',
            'today_date_field':'//html/body/table[2]/tbody/tr[2]/td[4]/p/span',
            'entry_id':'//html/body/table[2]/tbody/tr[2]/td[15]/p/span', #2431
            'approval_id':'//html/body/table[2]/tbody/tr[2]/td[16]/p/span', #0483
            'inputed_by':'//html/body/p[3]/span[2]'
            }
        self.browser.open_available_browser(url=url, browser_selection='edge')
        time.sleep(3)
        self.wait_and_click('//button[@id="details-button"]')
        self.wait_and_click('//*[@id="proceed-link"]')

        logger.info(f"logging in to oracle database to check approval ")
        self.browser.wait_until_element_is_visible(locator=xpath['username'],timeout=Constants.TIMEOUT)
        self.browser.input_text(locator=xpath['username'], text=username)
        self.browser.input_password(xpath['password'], password)

        self.browser.wait_until_element_is_visible(xpath['signin'])
        self.wait_and_click(xpath['signin'])
        logger.info(f'signin in to MIS ')
        display("signin in to MIS   ......................")

        self.browser.input_text(locator=xpath['input_field'], text='2431') #Rpa1
        self.browser.wait_until_element_is_visible(locator=xpath['input_field'],timeout=Constants.TIMEOUT)
        self.wait_and_click(xpath['view'])

        time.sleep(5)
        self.wait_and_select_frame(xpath['frame'])
        display("frame is selected ========")
        # self.browser.wait_until_element_is_visible(locator=xpath['inputed_by'],timeout=Constants.TIMEOUT)
        # display(self.browser.find_element(xpath['inputed_by']).text)
        self.browser.wait_until_element_is_visible(locator=xpath['today_date_field'],timeout=Constants.TIMEOUT)
        self.browser.wait_until_element_is_visible(locator=xpath['entry_id'],timeout=Constants.TIMEOUT)
        display(self.browser.find_element(xpath['today_date_field']).text)
        if(self.browser.find_element(xpath['today_date_field']).text == str(datetime.today().strftime('%Y-%m-%d'))):
            entry_id = self.browser.find_element(xpath['entry_id']).text
            display(entry_id) 
            approve_id = self.browser.find_element(xpath['approval_id']).text
            display(approve_id)
            if(entry_id == '2431'):
                if(approve_id == '0483'):
                    display(f"Approved by {approve_id} =========================")
                    return True
                else:
                    display("not approved ---------------")
                    return False
            else:
                display("not approved ------------------")
                return False
            
    # def run_advice(self):
    #     xl = win32com.client.Dispatch("Excel.Application")
    #     wb = xl.Workbooks.Open(r'path')
    #     xl.Application.Run('macro.xlsm!Module1.macro1("")')
    #     wb.Save()
    #     xl.Application.Quit()


    def logout(self):
        logger = self.run_item.logger if hasattr(self, 'run_item') else self.logger
        try:
            xpath = {
                'login_frame':"//iframe[@name='loginFrame']",
                'logout': '//a[@class="topnavi"]/img[@title="Logout"]'
            }

            logger.info("logging out...")
            self.browser.unselect_frame()
            self.wait_and_select_frame(xpath['login_frame'])
            self.wait_and_click(xpath['logout'])

            try:
                time.sleep(2)
                # allert_text=self.browser.alert_should_be_present()
                alert = self.browser.handle_alert(action="ACCEPT")
                logger.info(f'alert accepted: {alert}')
                logger.info(f'logged out....')
            except Exception as e:
                logger.error(f'error handling alert: {e}')
                raise e
        except Exception as e:
            logger.error("Failed to logout")
            logger.error(f"ERROR: {e}")
            
        
    def close_browser(self):
        logger = self.run_item.logger if hasattr(self, 'run_item') else self.logger
        try:
            self.browser.close_all_browsers()
        except Exception as e:
            logger.error("Failed to close browser")
            raise e
        
    def wait_and_click(self, xpath):
        logger = self.run_item.logger if hasattr(self, 'run_item') else self.logger
        try:
            self.browser.wait_until_element_is_visible(xpath, timeout=Constants.TIMEOUT)
            self.browser.click_element(xpath)
        except Exception as e:
            logger.error(f'error processing xpath: {xpath}')
            logger.error(e)
            raise e

    def wait_and_select_frame(self, xpath):
        logger = self.run_item.logger if hasattr(self, 'run_item') else self.logger
        try:
            self.browser.wait_until_element_is_visible(xpath, timeout=Constants.TIMEOUT)
            self.browser.select_frame(xpath)
            logger.info(f'selected {xpath} frame')
        except Exception as e:
            logger.error(f"failed to select {xpath} frame")
            raise e
    
    def wait_and_input(self,xpath,data):
        logger = self.run_item.logger if hasattr(self, 'run_item') else self.logger
        try:
            self.browser.wait_until_element_is_visible(xpath, timeout=Constants.TIMEOUT)
            self.browser.input_text(xpath,data)
            logger.info(f'Input {data}')
        except Exception as e:
            logger.error(f"Failed to input data in {xpath}")
            raise e