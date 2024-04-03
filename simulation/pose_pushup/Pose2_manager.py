from pyevsim import BehaviorModelExecutor, SystemSimulator, Infinite
from posture_check import Posture_Check_Model
from Pose_classify import Posture_Classify_Model
from return_result import Return_result_Model

class Pose2Manager():
    def __init__(self) -> None:
        # print(data)
        self.ss = SystemSimulator()

        self.ss.register_engine("CARE", "VIRTUAL_TIME", 0.1)

        self.health_model = self.ss.get_engine("CARE")

        self.health_model.insert_input_port("start")
        self.health_model.insert_input_port("_ing")
        self.health_model.insert_input_port("Done")
        self.health_model.insert_input_port("next")
        self.health_model.insert_input_port("stop")
        
        print("start engine")
        Check_m = Posture_Check_Model(0, Infinite, "Check_m", "CARE")
        Classify_m = Posture_Classify_Model(0, Infinite, "Classify_m", "CARE")
        Result_m = Return_result_Model(0, Infinite, "Result_m", "CARE")

        self.health_model.register_entity(Check_m)
        self.health_model.register_entity(Classify_m)
        self.health_model.register_entity(Result_m)

        # 이미지 데이터 수신 및 기존 조건과의 비교 및 결과 판독
        self.health_model.coupling_relation(None, "start", Check_m, "start")
        self.health_model.coupling_relation(Check_m, "pose_out", Classify_m, "start")
        self.health_model.coupling_relation(Classify_m, "pose_next_s", Check_m, "next")
        self.health_model.coupling_relation(Classify_m, "pose_next_f", Check_m, "-ing")
        self.health_model.coupling_relation(Classify_m, "pose_done", Result_m, "stop")

        self.start()


    def start(self) -> None:
        # pass
        self.health_model.insert_external_event("start","start")
        self.health_model.simulate()

if __name__ == '__main__':
    test_manager = Pose2Manager()