from qrlib.QRProcess import QRProcess
from qrlib.QRDecorators import run_item
from qrlib.QRRunItem import QRRunItem
from smartvistaComponent import SmartVistaComponent
from finacleComponent import finaclecomponent
from Email_component import EmailComponent
from Excel_component import ExcelComponent
from FTP_Component import FTPComponent
from qrlib.QRUtils import get_secret, display
import Constants
from datetime import datetime,timedelta
from Utils import (
    delete_files_in_folder,
    check_file_downloaded_or_not,
    generate_report_name
)

class DefaultProcess(QRProcess):

    def __init__(self):
        super().__init__()
        self.data = []
        self.merchant_mail_list = None
        self.ips_mail_list = None
        self.prepaid_mail_list = None
        self.smartvista_component = SmartVistaComponent()
        self.finacle_component = finaclecomponent()
        self.email_component = EmailComponent()
        self.register(self.email_component)
        self.excel_component = ExcelComponent()
        self.ftp_component = FTPComponent()
        self.register(self.excel_component)
        self.register(self.ftp_component)
        self.register(self.smartvista_component)
        self.register(self.finacle_component)

    @run_item(is_ticket=False)
    def before_run(self, *args, **kwargs):
        run_item: QRRunItem = kwargs["run_item"]
        self.notify(run_item)
        logger = run_item.logger
        delete_files_in_folder(logger,Constants.download_path)
        
        current_date = datetime.now()
        year = current_date.strftime("%Y")
        month = current_date.strftime("%B").lower()
        day = current_date.strftime("%d")
        try:
            report_directory = generate_report_name(numb=0)
            path = f"{year}/{month}/{day}/{report_directory}/{report_directory}"
            file_name = f'CPD_Issuing_SBL {report_directory.split()[-1]}.xlsx'
            display(f"from default procee {file_name}")
            with self.ftp_component as ftp:
                ftp.set_cwd(path)
                ftp.list_and_download_dailyreport(Constants.download_path, file_name)
                
            check_file_downloaded_or_not(logger,'.xlsx')
            file_name= check_file_downloaded_or_not(logger, '.xlsx')
            print(f"Downloaded file name: {file_name}")
            
        except Exception as e1:
            print(f"First attempt failed: {str(e1)}")
            for i in range(1, 10):
                try:
                    report_directory = generate_report_name(numb=i)
                    path = f"{year}/{month}/{day}/{report_directory}/{report_directory}"
                    file_name = f'CPD_Issuing_SBL {report_directory.split()[-1]}.xlsx'
                    with self.ftp_component as ftp:
                        ftp.set_cwd(path)
                        ftp.list_and_download_dailyreport(Constants.download_path, file_name)
                    
                    file_name = check_file_downloaded_or_not(logger, '.xlsx')
                    print(f"Downloaded file name: {file_name}")
                    break  

                except Exception as e2:
                    print(f"Attempt {i} failed: {str(e2)}")
                    if i == 10:
                        print("All attempts failed. No file downloaded.")


    @run_item(is_ticket=False, post_success=False)
    def before_run_item(self, *args, **kwargs):
        run_item = QRRunItem(is_ticket=True)
        self.notify(run_item)
        logger = run_item.logger
        
        amount = self.excel_component.read_excel_file()
        self.finacle_component.open_finacle()
        self.finacle_component.login()
        self.finacle_component.navigate_to_hxfer()
        self.finacle_component.transfer_trans_value(amount)
        self.finacle_component.logout()
        self.finacle_component.close_browser()

        
        run_item.report_data["Process Status"] = f" Ticket Generation and FTP upload Complete"
        report_data = {'Filename': '','Date':''}
        run_item.report_data = report_data
        run_item.set_success()
        run_item.post()

    @run_item(is_ticket=True)
    def execute_run_item(self, *args, **kwargs):
        run_item: QRRunItem = kwargs["run_item"]
        self.notify(run_item)
        

    @run_item(is_ticket=False, post_success=False)
    def after_run_item(self, *args, **kwargs):
        run_item: QRRunItem = kwargs["run_item"]
        self.notify(run_item)

        # moved_path = 'test/' #set ftp working dir to outward/transaction 

        # current_date = datetime.now()
        # year = current_date.strftime("%Y")
        # month = current_date.strftime("%B").lower()
        # day = current_date.strftime("%m-%d-%Y")

        # year_directory = year
        # month_directory = f"{year}/{month}"
        # day_directory = f"{year}/{month}/{day}"

        # Ensure remote directory structure exists
        # with self.ftp_component as ftp:
        #     ftp.create_directory_if_not_exists(year_directory)
        #     ftp.set_cwd(year_directory)
        #     ftp.create_directory_if_not_exists(month)
        #     ftp.set_cwd(month_directory)
        #     ftp.create_directory_if_not_exists(day)
        #     ftp.set_cwd(day_directory)
        #     # moved_path = f"test/{year}/{month}/{day}"
        #     # display(moved_path)
        #     ftp.upload_file(Constants.all_files_path,f'{Constants.final_file}')
        # # logger.info(f'{moved_path} files uploaded to ftp')
        # display(f'{moved_path} files uploaded to ftp')

        # moved_path = 'Bulk_upload_files/' #set ftp working dir to outward/transaction 
        # display(moved_path)
        # with self.ftp_component as ftp:
        #     ftp.set_cwd(f'{moved_path}')
        #     ftp.upload_file_datewise(Constants.all_files_path,f'{Constants.bulk_file}',moved_path)
        # # logger.info(f'{moved_path} files uploaded to ftp')
        # display(f'{moved_path} files uploaded to ftp')

        
        # self.ips_mail_list =  [{'account_name':'ANUKRIT TRADE PVT LTD', 'amount':'500'}]
        # self.email_component.ips_transaction_mail(self.ips_mail_list)

    @run_item(is_ticket=False, post_success=False)
    def after_run(self, *args, **kwargs):
        run_item: QRRunItem = kwargs["run_item"]
        self.notify(run_item)

        self.finacle_component.logout()
        # self.smartvista_component.logout_smartvista()
        # self.finacle_component.close_browser()
 

    def execute_run(self):
        run_item = QRRunItem(is_ticket=True)
        self.notify(run_item)
        logger = run_item.logger

        self.finacle_component.open_finacle()
        self.finacle_component.login()
        self.finacle_component.navigate_to_httum()
        self.finacle_component.upload_batch()
        check = self.finacle_component.check_batch_upload(value=1)
        if(not check):
            display("not skipped ")
            check = self.finacle_component.check_batch_upload(value=0)
        display("done !!!!!!!!!!!!")

        # self.email_component.mail_to_approval()
        self.finacle_component.logout()
        self.finacle_component.close_browser()
# self.finacle_component.open_mis_check_approval()
# self.finacle_component.close_browser()

        # self.merchant_mail_list = self.excel_component.mail_list_merchant()
        # self.email_component.mail_to_merchant_more_than_30_days(self.merchant_mail_list)
        # self.email_component.summary_mail()

        moved_path = 'test/' #set ftp working dir to outward/transaction 

        current_date = datetime.now()
        year = current_date.strftime("%Y")
        month = current_date.strftime("%B").lower()
        day = current_date.strftime("%m-%d-%Y")

        year_directory = year
        month_directory = f"{year}/{month}"
        day_directory = f"{year}/{month}/{day}"

        # Ensure remote directory structure exists
        with self.ftp_component as ftp:
            ftp.create_directory_if_not_exists(year_directory)
            ftp.set_cwd(year_directory)
            ftp.create_directory_if_not_exists(month)
            ftp.set_cwd(month_directory)
            ftp.create_directory_if_not_exists(day)
            ftp.set_cwd(day_directory)
            # moved_path = f"test/{year}/{month}/{day}"
            # display(moved_path)
            ftp.upload_file(Constants.all_files_path,f'{Constants.final_file}')

        # moved_path = 'Bulk_upload_files/' #set ftp working dir to outward/transaction 
        # display(moved_path)
        # with self.ftp_component as ftp:
        #     ftp.set_cwd(f'{moved_path}')
        #     ftp.upload_file_datewise(Constants.all_files_path,f'{Constants.bulk_file}')
        # logger.info(f'{moved_path} files uploaded to ftp')
        # display(f'{moved_path} files uploaded to ftp')

        for dict in self.ips_mail_list:
            display(f"sending mail to == {dict}")
            logger.info(f"sending mail to == {dict}")
            self.email_component.ips_transaction_mail(dict)

        for dict in self.prepaid_mail_list:
            display(f"sending mail to == {dict}")
            logger.info(f"sending mail to == {dict}")
            self.email_component.prepaid_case(dict)

        run_item.report_data["Process Status"] = f" Pos Settlement complete"
        report_data = {'Filename': '','Date':''}
        run_item.report_data = report_data
        run_item.set_success()
        run_item.post()

