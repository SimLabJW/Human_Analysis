from pyevsim import BehaviorModelExecutor, SystemSimulator, Infinite
from posture_check import Posture_Check_Model
from Pose_classify import Posture_Classify_Model
from image_angle import Image_Pose_Angle_Model

class PoseManager():
    def __init__(self) -> None:
        
        self.ss = SystemSimulator()

        self.ss.register_engine("CARE", "VIRTUAL_TIME", 1)
        self.health_model = self.ss.get_engine("CARE")

        self.health_model.insert_input_port("start")
        self.health_model.insert_input_port("_ing")
        self.health_model.insert_input_port("Done")
        
        print("start engine")
        Check_m = Posture_Check_Model(0, Infinite, "Check_m", "CARE")
        Classify_m = Posture_Classify_Model(0, Infinite, "Classify_m", "CARE")
        Default_m = Image_Pose_Angle_Model(0,Infinite, "Default", "CARE")

        self.health_model.register_entity(Check_m)
        self.health_model.register_entity(Classify_m)
        self.health_model.register_entity(Default_m)

        self.health_model.coupling_relation(None, "start", Default_m, "start")
        # self.health_model.coupling_relation(None, "start", Check_m, "start")
        # self.health_model.coupling_relation(None, "start", Classify_m, "start")
        # self.health_model.coupling_relation(Classify_m, "pose_next", Classify_m, "_ing")
        # self.health_model.coupling_relation(Classify_m, "pose_done", Classify_m, "Done")

        self.start()

    def start(self) -> None:

        self.health_model.insert_external_event("start","start")
        self.health_model.simulate()
