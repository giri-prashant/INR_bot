from datetime import datetime,timedelta
TIMEOUT = 60
today_date = datetime.now()
one_day_ago = today_date - timedelta(days=1)
two_day_ago = today_date - timedelta(days=2)
DATE = one_day_ago.strftime("%d%m%Y")
NARR_DATE = one_day_ago.strftime("%d.%m.%Y")


# DOWNLOADDIR = 'C:\\Users\\niraj.sharma\\QuickFox\\bot-starter-kit-v2.0-optimize\\download_dir'
DB_PATH = ''
db_table_name = 'daily_report'
download_path= r'C:\Users\niraj.sharma\QuickFox\Pos_settlement\download_path'

file_path = f"C:\\Users\\niraj.sharma\\QuickFox\\Pos_settlement\\download_path\\CPD_Issuing_SBL 14_{DATE}.xlsx"

