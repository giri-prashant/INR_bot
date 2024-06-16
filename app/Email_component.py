import imaplib

from robot.libraries.BuiltIn import BuiltIn

from qrlib.QREnv import QREnv
from qrlib.QRComponent import QRComponent
from RPA.Email.ImapSmtp import ImapSmtp


display = BuiltIn().log_to_console


class EmailComponent(QRComponent):
    def __init__(self):
        super().__init__()
        # send mail values
        self.body = ''
        self.recipients = '' #sender = rpa.operation@pcbl.com.np  
        
        # smtp connection
        self.account = ''
        self.password = ''
        self.server = ''
        self.port = ''
        self.cc = ''
        self.__vault_data = {}
        # self.__vault_data_imap = {}

    def _get_vault(self):
        # self.logger = self.run_item.logger
        self.__vault_data: dict = QREnv.VAULTS['smtp']
        # self.logger.info("Got vault data")
        display('Got vault data ')
    def _imap_from_vault(self):
        # self.logger = self.run_item.logger
        self.__vault_data: dict = QREnv.VAULTS['imap']
        display('Get imap vault successfully')
        # self.logger.info('Get imap vault successfully')
        

    def _get_imap_creds(self):
        # self.logger = self.run_item.logger
        self.imap_account = self.__vault_data['mail_account']
        self.imap_server = self.__vault_data['mail_host']
        self.imap_port = self.__vault_data['imap_port']
        self.imap_password = self.__vault_data['mail_password']
       
        display('get imap creadential successulfy')
        self.logger.info('get imap creadential successulfy')

    def imap_login(self):
        self.logger = self.run_item.logger
        self._imap_from_vault()
        imap = imaplib.IMAP4(self.__vault_data['mail_host'],int(self.__vault_data['imap_port']))
        imap.login(self.__vault_data['mail_account'],self.__vault_data['mail_password'])
        display('Logging imap cread successfully')
        self.imap = imap

    def _set_smtp_creds(self):
        # logger = self.run_item.logger
        self.account = self.__vault_data['account']
        self.server = self.__vault_data['server']
        self.port = self.__vault_data['port']
        # self.configpath = self.__vault_data['config_path']
        try:
            self.password = self.__vault_data['password']
        except:
            self.password = None

    def mail_to_approval(self):
        self._get_vault()
        self._set_smtp_creds()

        self.mail = ImapSmtp(smtp_server=self.server, smtp_port=int(self.port))
        self.mail.authorize_smtp(account=self.account, password=str(self.password), smtp_server=self.server, smtp_port=int(self.port),)
        self.subject = '''Request for approval'''
       
        #done        
        self.body = f''' 
                    
            <span>
            Dear Recipient,<br>
            <p>
                The batch file has been uploaded please verify.
            </p>
            Thank you for your attention.<br>

            </span>

                    '''
        self.mail.send_message(
            sender=self.account,
            recipients='',#'suraj.kaphle@pcbl.com.np',
            # cc='',
            subject=self.subject,
            body=self.body,
            # attachments=self.sending_file_list,
            html=True
        )
        display("mail sent")

    def mail_to_merchant_more_than_30_days(self,receivers):
        # logger = self.run_item.logger
        self._get_vault()
        self._set_smtp_creds()
        receivers = ''
        for merchant in receivers:
            receivers += merchant + ';'

        self.mail = ImapSmtp(smtp_server=self.server, smtp_port=int(self.port))
        self.mail.authorize_smtp(account=self.account, password=str(self.password), smtp_server=self.server, smtp_port=int(self.port),)
        # self.sending_file_list.append(attachments_path)
        self.subject = ''' settlement date more than 30 days  '''
        self.body = f''' 
                      
                    '''
        self.mail.send_message(
            sender=self.account,
            recipients=receivers,
            # cc='',
            subject=self.subject,
            body=self.body,
            # attachments=self.sending_file_list,
            html=True
        )

    def summary_mail(self):
        logger = self.run_item.logger
        self._get_vault()
        self._set_smtp_creds()
        # self.sending_file_list.append(attachment)
        self.mail = ImapSmtp(smtp_server=self.server, smtp_port=int(self.port))
        self.mail.authorize_smtp(account=self.account, password=str(self.password), smtp_server=self.server, smtp_port=int(self.port),)
        self.subject = '''' task completed  '''
        self.body = f''' 
            The batch has been uploaded. Pleaser verify !!!! 
                    '''
        self.mail.send_message(
            sender=self.account,
            recipients='punam.shrivastav@sbl.com.np',
            # cc='',
            subject=self.subject,
            # attachments=self.sending_file_list,
            body=self.body,
            html=True
        )

    def prepaid_case(self,dict):
        # logger = self.run_item.logger
        self._get_vault()
        self._set_smtp_creds()
        self.mail = ImapSmtp(smtp_server=self.server, smtp_port=int(self.port))
        self.mail.authorize_smtp(account=self.account, password=str(self.password), smtp_server=self.server, smtp_port=int(self.port),)
        # self.sending_file_list.append(attachments_path)

        self.subject = f''' IPS Transfer {dict['account_name']}  '''
        self.body = f''' 
                    Dear team,<br>
                    The actual  Dollar amount of {dict['Ref Num']} and {dict['account_number']} is USD {dict['amount']}. Please Modify it for now!!

                    Note: This is automated mail sent by BOT.<br>
                    
                    '''
        self.mail.send_message(
            sender=self.account,
            recipients='umesh.maharjan@sbl.com.np', #;punam.shrivastav@sbl.com.np',
            # cc='',
            subject=self.subject,
            body=self.body,
            # attachments=self.sending_file_list,
            html=True
            )

    def ips_transaction_mail(self,dict):
        # logger = self.run_item.logger
        self._get_vault()
        self._set_smtp_creds()
        self.mail = ImapSmtp(smtp_server=self.server, smtp_port=int(self.port))
        self.mail.authorize_smtp(account=self.account, password=str(self.password), smtp_server=self.server, smtp_port=int(self.port),)
        # self.sending_file_list.append(attachments_path)
        if(dict['account_name'] == 'ANUKRIT TRADE PVT LTD'):
            Account_number = '0760146190800017'
        else:
            Account_number =  '03601040262682'

        self.subject = f''' IPS Transfer {dict['account_name']}  '''
        self.body = f''' 
                    Dear team,<br>

                    As per the instruction from our POS acquiring merchant: ANUKRIT TRADE PVT
                    LTD, kindly transfer Nrs. {dict['amount'] } /- IDT (00101440900002) to the following
                    details deducting the necessary charges.<br>

                    Account Name:{dict['account_name'] }<br>

                    Account Number: {Account_number}<br>

                    Creditor Bank: NMB Bank Limited.<br>

                    Note: This is automated mail sent by BOT.<br>
                    
                    '''
        self.mail.send_message(
            sender=self.account,
            recipients='umesh.maharjan@sbl.com.np', #;punam.shrivastav@sbl.com.np',
            # cc='',
            subject=self.subject,
            body=self.body,
            # attachments=self.sending_file_list,
            html=True
            )