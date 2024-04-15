from pyevsim import BehaviorModelExecutor, SystemSimulator, Infinite
from posture_check import Posture_Check_Model
from pose_danger import Pose_Danger_Model

class DangerManager():
    def __init__(self) -> None:
        # print(data)
        self.ds = SystemSimulator()

        self.ds.register_engine("DANGER", "VIRTUAL_TIME", 0.1)

        self.danger_model = self.ds.get_engine("DANGER")

        self.danger_model.insert_input_port("start")
        
        print("start engine_arm_leg")
        Check_m = Posture_Check_Model(0, Infinite, "Check_m", "DANGER")
        Danger_m = Pose_Danger_Model(0, Infinite, "Classify_m", "DANGER")
     

        self.danger_model.register_entity(Check_m)
        self.danger_model.register_entity(Danger_m)


        self.danger_model.coupling_relation(None, "start", Check_m, "start")
        self.danger_model.coupling_relation(Check_m, "pose_out", Danger_m, "start")

        self.start()


    def start(self) -> None:
        # pass
        self.danger_model.insert_external_event("start","start")
        self.danger_model.simulate()

if __name__ == '__main__':
    test_manager = DangerManager()