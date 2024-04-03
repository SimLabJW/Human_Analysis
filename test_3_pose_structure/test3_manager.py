from pyevsim import BehaviorModelExecutor, SystemSimulator, Infinite
from test_model_3 import TEST3_Model

class TEST3Manager():
    def __init__(self) -> None:

        self.test_3_simulator =  SystemSimulator()

        self.test_3_simulator.register_engine(f"TEST3", "VIRTUAL_TIME", 0.1)

        self.test_3_model = self.test_3_simulator.get_engine(f"TEST3")
        self.test_3_model.insert_input_port("start")


        TEST3_M = TEST3_Model(0, Infinite, "TEST3_M", "TEST3")
        self.test_3_model.register_entity(TEST3_M)
        self.test_3_model.coupling_relation(None, "start", TEST3_M, "start")

        self.start()


    def start(self):

        self.test_3_model.insert_external_event("start", "start")
        self.test_3_model.simulate()
        
if __name__ == '__main__':
    test_manager = TEST3Manager()