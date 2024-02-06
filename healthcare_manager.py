from pyevsim import BehaviorModelExecutor, SystemSimulator, Infinite
from posture_check import Posture_Check_Model

class PoseManager():
    def __init__(self) -> None:
        
        self.ss = SystemSimulator()

        self.ss.register_engine("CARE", "VIRTUAL_TIME", 1)
        self.health_model = self.ss.get_engine("CARE")

        self.health_model.insert_input_port("start")
        
        print("start engine")
        Cm = Posture_Check_Model(0, Infinite, "CM", "CARE")

        self.health_model.register_entity(Cm)

        self.health_model.coupling_relation(None, "start", Cm, "start")

        self.start()

    def start(self) -> None:

        self.health_model.insert_external_event("start","start")
        self.health_model.simulate()
