from pyevsim import BehaviorModelExecutor, Infinite, SysMessage
from config import *
import json
import random
import string

class Return_result_Model(BehaviorModelExecutor):
    def __init__(self, instance_time, destruct_time, name, engine_name):
        BehaviorModelExecutor.__init__(self, instance_time, destruct_time, name, engine_name)
        
        self.init_state("Wait")
        self.insert_state("Wait", Infinite)
        # self.insert_state("Generate",1)
        self.insert_input_port("stop")

        self.result_dic = {}
        
    def ext_trans(self, port, msg):
        
        if port == "stop":
            # 동작 기준 정보 불러오기
            self.result = msg.retrieve()
            # 보낼 정보 모음집
            for key in Key_LIST:
                if key == 'Way':
                    # 랜덤으로 4, 5, 6 중에서 하나의 숫자 선택
                    way_values = random.sample([4, 5, 6], 2)
                    self.result_dic[key] = way_values
                elif key == 'Health':
                    self.result_dic[key] = 100
                elif key == 'S/F':
                    self.result_dic[key] = self.result
                elif key == 'Pose_Data':
                    self.result_dic[key] = [
                        [1, 2],
                        [3, 4],
                        [5, 6]
                    ]
                else:
                    # 랜덤 문자열 생성
                    random_string = ''.join(random.choices(string.ascii_lowercase, k=5))
                    self.result_dic[key] = random_string

            json_file_path = RESULT_JSON
            with open(json_file_path, 'w') as json_file:
                json.dump(self.result_dic, json_file, indent=2)
            # Manager().save_data(self.result)
            self._cur_state = "Wait"
            


      
    def output(self): 
        # if self._cur_state == "Generate":
        #     self._cur_state = "Wait"
        
        if self._cur_state == "Wait":
            
            self._cur_state = "Wait"


            
    def int_trans(self):
        if self._cur_state == "Wait":
            self._cur_state = "Wait"
        if self._cur_state == "Generate":
            self._cur_state = "Generate"

    def save_result(self):
        return self.result
 
        