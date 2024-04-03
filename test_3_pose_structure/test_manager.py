from pyevsim import BehaviorModelExecutor, SystemSimulator, Infinite
from test_model_1 import TEST1_Model

class TEST1Manager():
    def __init__(self) -> None:

        self.test_1_simulator =  SystemSimulator()
      
        self.test_1_simulator.register_engine(f"TEST1", "VIRTUAL_TIME", 0.1)
 
        self.test_1_model = self.test_1_simulator.get_engine(f"TEST1")
        self.test_1_model.insert_input_port("start")

        TEST1_M = TEST1_Model(0, Infinite, "TEST1_M", "TEST1")
        self.test_1_model.register_entity(TEST1_M)
        self.test_1_model.coupling_relation(None, "start", TEST1_M, "start")

        self.start()

    def start(self):
        # 병렬좀 해봐 현기
        self.test_1_model.insert_external_event("start", "start")
        self.test_1_model.simulate()

        
if __name__ == '__main__':
    test_manager = TEST1Manager()