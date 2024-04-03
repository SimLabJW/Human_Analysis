from pyevsim import BehaviorModelExecutor, SystemSimulator, Infinite
from test_model_2 import TEST2_Model


class TEST2Manager():
    def __init__(self) -> None:

        self.test_2_simulator =  SystemSimulator()

        self.test_2_simulator.register_engine(f"TEST2", "VIRTUAL_TIME", 0.1)

        self.test_2_model = self.test_2_simulator.get_engine(f"TEST2")
        self.test_2_model.insert_input_port("start")

        TEST2_M = TEST2_Model(0, Infinite, "TEST2_M", "TEST2")
        self.test_2_model.register_entity(TEST2_M)
        self.test_2_model.coupling_relation(None, "start", TEST2_M, "start")



        self.start()


    def start(self):

        self.test_2_model.insert_external_event("start", "start")
        self.test_2_model.simulate()

if __name__ == '__main__':
    test_manager = TEST2Manager()