from pyevsim import BehaviorModelExecutor, Infinite, SysMessage
import numpy as np
import math
import matplotlib as plt
from config import *
import json

class Posture_Classify_Model(BehaviorModelExecutor):
    def __init__(self, instance_time, destruct_time, name, engine_name):
        BehaviorModelExecutor.__init__(self, instance_time, destruct_time, name, engine_name)
        
        self.init_state("Wait")
        self.insert_state("Wait", Infinite)

        self.insert_state("Stop", Infinite)
        self.insert_state("Generate",0)
        self.insert_state("Next_s",1)
        self.insert_state("Next_f",1)
        self.insert_input_port("start")
        self.insert_input_port("-ing")
        self.insert_input_port("Done")

        self.insert_output_port("pose_next_s")
        self.insert_output_port("pose_next_f")
        self.insert_output_port("pose_done")
       
        # 기존 정보들에 대한 정보

        self.default_pose = "arm_leg_.png"
        self.default_count = 0
        self.default_angle = []

        self.pose_determine()
        # 입력 값에 대한 정보 수정
        self.landmarks = []
        self.count = 0

        #상태확인
        self.next_step = True
        
    def ext_trans(self, port, msg):
        
        if port == "start":
            # 동작 기준 정보 불러오기
            self.landmarks_frame = msg.retrieve()
            self.count = self.landmarks_frame[0][0]
            self.landmarks_frame = self.landmarks_frame[0][1]
            # print(self.landmarks_frame)
            self._cur_state = "Generate"

        # if port == "landmarks":
        #     self.landmarks_frame = msg.retrieve()
        #     self.pose_classify(self.landmarks_frame[0][1])
      
    def output(self): 

        if self._cur_state == "Generate":
            # 조건 자동삽입
            if (self.count +1) < self.default_count:
                # print("---------------------------------")

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
                self.next_step = False
                self._cur_state = "Wait"  
            
        if self._cur_state == "Next_s":
            msg = SysMessage(self.get_name(), "pose_next_s")
            msg.insert(["Succes", self.count+1])
            return msg
        
        if self._cur_state == "Next_f":
            msg = SysMessage(self.get_name(), "pose_next_f")
            msg.insert(["Fail", self.count])
            return msg
            
    def int_trans(self):
        if self._cur_state == "Generate":
            self._cur_state = "Generate"
        elif self._cur_state == "Wait":
            self._cur_state = "Wait"
        elif self._cur_state == "Stop":
            self._cur_state = "Stop"
            
    
    def pose_determine(self):

        # JSON 파일 경로
        json_file_path = ANGLE_JSON
        # JSON 파일 읽어오기
        with open(json_file_path, 'r') as json_file:
            loaded_data = json.load(json_file)

        default_pose_info = loaded_data[self.default_pose]
        self.default_count = default_pose_info["count"]

        for angle in range(self.default_count):
            self.default_angle.append(default_pose_info['files'][angle])
        # print(self.default_angle[0])
  
    def contrast_angle(self, input_data, default_data,threshold):
        # print(f"default data\n{default_data}")
        individual_avgs = [[sum(item) / len(item) for item in sublist] for sublist in [input_data, default_data]]
        for i in range(len(individual_avgs)):

            lower_limit = individual_avgs[1][i] - threshold
            upper_limit = individual_avgs[1][i] + threshold
            
            if lower_limit < 0:
                lower_limit = 0

            if not (lower_limit <= individual_avgs[0][i] <= upper_limit):
                # print(f"{lower_limit} {individual_avgs[0][i]} {upper_limit}")
                return False

        return True

        