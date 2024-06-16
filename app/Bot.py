from qrlib.QRBot import QRBot
from DefaultProcess import DefaultProcess

from qrlib.QRUtils import get_secret, display


class Bot(QRBot):

    def __init__(self):
        super().__init__()
        self.process = DefaultProcess()

    def start(self):
        self.setup_platform_components()
        self.process.before_run()

        # self.process.before_run_item()
        # self.process.execute_run()



        # self.process.after_run_item()





    def teardown(self):
        self.process.after_run()
        
        pass
