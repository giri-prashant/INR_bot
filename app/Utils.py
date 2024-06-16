
from glob import glob
import subprocess
import time
import psutil
import re
import os
import shutil


import Constants

        
def check_file_downloaded_or_not( logger,file_extension):
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


def delete_files_in_folder(logger, folder_path):
    path = folder_path
    files = os.listdir(path=path)
    for file in files:
        file_path = os.path.join(path, file)
        os.remove(file_path)
        logger.info(f'{file} deleted')

def rename_and_move(chequenumber, logger):
    path = Constants.pdf_download_dir
    files = os.listdir(path=path)
    for file in files:
        file_path = os.path.join(path, file)
        if os.path.isfile(file_path):
            name = f'{chequenumber}.pdf'
            renamed = os.path.join(path, name )
            os.rename(file_path, renamed)
            logger.info(f'new pdf name: {name} and path is: {renamed}')
            if not os.path.exists(Constants.sanitize_folder):
                os.mkdirs(Constants.sanitize_folder)
            moved_name = os.path.join(Constants.sanitize_folder, name )
            shutil.move(renamed, moved_name)

def close_chrome():
    call = 'TASKLIST', '/FI', 'imagename eq chrome.exe'
    tasks = subprocess.check_output(call).decode().split("\r\n")
    arr1 = []
    for task in tasks:
        m = re.match("(.+?) +(\d+) (.+?) +(\d+) +(\d+.* K).*",task)
        if m is not None:
            arr1.append({"image":m.group(1),
                        "pid":m.group(2),
                        "session_name":m.group(3),
                        "session_num":m.group(4),
                        "mem_usage":m.group(5)
                        })
    for item in arr1:
        call1 = 'wmic path Win32_PerfFormattedData_PerfProc_Process where "IDProcess=%s" get PercentProcessorTime' % item["pid"]

        output1 = subprocess.check_output(call1).decode()

        last_line = output1.strip().split('\r\n')[-1]
        print(last_line)
        print(type(last_line))

        if len(last_line) > 0:
            percent = int(last_line)
            if percent >=65:
                print("taskkill")
                subprocess.run(['taskkill', '/pid', f'{item["pid"]}', '/f'])