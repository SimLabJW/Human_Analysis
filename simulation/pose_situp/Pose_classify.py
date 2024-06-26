from pyevsim import BehaviorModelExecutor, Infinite, SysMessage
# from config import *

class Posture_Classify_Model(BehaviorModelExecutor):
    def __init__(self, instance_time, destruct_time, name, engine_name):
        BehaviorModelExecutor.__init__(self, instance_time, destruct_time, name, engine_name)
        
        self.init_state("Wait")

        self.insert_state("Wait", Infinite)
        self.insert_state("Generate",1)
        
        self.insert_state("Next_s",1)
        self.insert_state("Next_f",1)
        self.insert_state("Stop",1)

        self.insert_input_port("start")
        self.insert_input_port("-ing")
        self.insert_input_port("Done")

        self.insert_output_port("pose_next_s")
        self.insert_output_port("pose_next_f")
        self.insert_output_port("pose_done")
       
        # 기존 정보들에 대한 정보

        # self.default_pose = "arm_leg_.png"
        self.default_count = 0
        self.default_angle = []

        self.pose_determine()
        # 입력 값에 대한 정보 수정
        self.landmarks = []
        self.count = 0
        
    def ext_trans(self, port, msg):
        
        if port == "start":
            # 동작 기준 정보 불러오기
            self.landmarks_frame = msg.retrieve()
            self.count = self.landmarks_frame[0][0]
            self.landmarks_frame = self.landmarks_frame[0][1]
  
            self._cur_state = "Generate"

      
    def output(self): 

        if self._cur_state == "Generate":
            # 조건 자동삽입
            if self.count  < self.default_count:
                result = self.contrast_angle(self.landmarks_frame,\
                                            self.default_angle[self.count][1],15)
                if result:
                    print("주어진 데이터는 기준 데이터의 범위 안에 있습니다.")
                    self._cur_state = "Next_s" 
                else:
                    # print("주어진 데이터는 기준 데이터의 범위를 벗어납니다.")
                    self._cur_state = "Next_f" 

            else:
                print("pose simulation Done")
                self._cur_state = "Stop"  
            
        elif self._cur_state == "Next_s":
            msg = SysMessage(self.get_name(), "pose_next_s")
            msg.insert(["Succes", self.count+1])
            return msg
        
        elif self._cur_state == "Next_f":
            msg = SysMessage(self.get_name(), "pose_next_f")
            msg.insert(["Fail", self.count])
            return msg
        
        elif self._cur_state == "Stop":
            msg = SysMessage(self.get_name(), "pose_done")
            msg.insert("Fail or Succes")
            return msg
            
    def int_trans(self):
        if self._cur_state == "Generate":
            self._cur_state = "Wait"
        elif self._cur_state == "Wait":
            self._cur_state = "Wait"
        elif self._cur_state == "Stop":
            self._cur_state = "Wait"
            
    
    def pose_determine(self):

        self.default_count = 3

        situp_angle = [
            [1,
             [[42.97829555927652,266.12266671474754],[147.3339864989657,152.17590361574673],[62.74269707402858,61.04384216059509]]
             ],
             [2,
              [[48.2162199400034,47.90191046888365],[359.5581389950517,7.32025816475247],[284.33034128687405,283.51382207436495]]
              ],
              [3,
               [[42.97829555927652,266.12266671474754],[147.3339864989657,152.17590361574673],[62.74269707402858,61.04384216059509]]
               ]
               ]
        
        self.default_angle.append(situp_angle)

  
    def contrast_angle(self, input_data, default_data,threshold):

        individual_avgs = [[sum(item) / len(item) for item in sublist] for sublist in [input_data, default_data]]
        for i in range(len(individual_avgs)):

            lower_limit = individual_avgs[1][i] - threshold
            upper_limit = individual_avgs[1][i] + threshold
            
            if lower_limit < 0:
                lower_limit = 0

            if not (lower_limit <= individual_avgs[0][i] <= upper_limit):
                return False

        return True

        