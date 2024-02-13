import logging
from healthcare_manager import PoseManager
# from data_manager import Manager
# import threading
# print("aaaa")
logging.basicConfig(
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
        )
logger = logging.getLogger(__name__)

class Simulation():
    def __init__(self,data) -> None:

        self.data = data
        hm = PoseManager(self.data)
       
        

    
