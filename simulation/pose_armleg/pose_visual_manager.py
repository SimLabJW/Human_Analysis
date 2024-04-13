from pyevsim import BehaviorModelExecutor, SystemSimulator, Infinite
from visual_model import *

class PoseVisualManager():
    def __init__(self) -> None:
        # print(data)
        self.vs = SystemSimulator()

        self.vs.register_engine("VISUAL", "VIRTUAL_TIME", 0.1)

        self.visual_model = self.vs.get_engine("VISUAL")

        self.visual_model.insert_input_port("start")
   
        print("start visual engine_arm_leg")
        Visual_m = Visual_Model(0, Infinite, "Check_m", "CARE")

        self.visual_model.register_entity(Visual_m)


        # 이미지 데이터 수신 및 기존 조건과의 비교 및 결과 판독
        self.visual_model.coupling_relation(None, "start", Visual_m, "start")

        self.start()


    def start(self) -> None:
        # pass
        self.visual_model.insert_external_event("start","start")
        self.visual_model.simulate()


if __name__ == '__main__':
    test_manager = PoseVisualManager()