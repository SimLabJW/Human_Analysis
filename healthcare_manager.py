from pyevsim import BehaviorModelExecutor, SystemSimulator, Infinite
from posture_check import Posture_Check_Model
from Pose_classify import Posture_Classify_Model
from image_angle import Image_Pose_Angle_Model
from image_folder import Reading_Folder_Model

class PoseManager():
    def __init__(self) -> None:
        
        self.ss = SystemSimulator()
        # self.ris = SystemSimulator()

        self.ss.register_engine("CARE", "VIRTUAL_TIME", 1)
        # self.ris.register_engine("READ", "VIRTUAL_TIME", 1)

        self.health_model = self.ss.get_engine("CARE")
        # self.reading_model = self.ris.get_engine("READ")

        self.health_model.insert_input_port("start")
        self.health_model.insert_input_port("_ing")
        self.health_model.insert_input_port("Done")

        # self.reading_model.insert_input_port("start")
        
        print("start engine")
        Check_m = Posture_Check_Model(0, Infinite, "Check_m", "CARE")
        Classify_m = Posture_Classify_Model(0, Infinite, "Classify_m", "CARE")

        # Default_m = Image_Pose_Angle_Model(0,Infinite, "Default", "READ")
        # Reading_m = Reading_Folder_Model(0,Infinite, "Reading_m", "READ")

        self.health_model.register_entity(Check_m)
        self.health_model.register_entity(Classify_m)

        # self.reading_model.register_entity(Default_m)
        # self.reading_model.register_entity(Reading_m)


        # 이미지 자동 각도 계산을 위한 모델 생성.
        # self.reading_model.coupling_relation(None, "start", Default_m, "start")
        # self.reading_model.coupling_relation(None, "start", Reading_m, "start")

        # 이미지 데이터 수신 및 기존 조건과의 비교 및 결과 판독
        self.health_model.coupling_relation(None, "start", Check_m, "start")
        self.health_model.coupling_relation(None, "start", Classify_m, "start")
        self.health_model.coupling_relation(Classify_m, "pose_next", Classify_m, "_ing")
        self.health_model.coupling_relation(Classify_m, "pose_done", Classify_m, "Done")

        self.start()

    def start(self) -> None:

        self.health_model.insert_external_event("start","start")
        self.health_model.simulate()

        # self.reading_model.insert_external_event("start", "start")
        # self.reading_model.simulate()
