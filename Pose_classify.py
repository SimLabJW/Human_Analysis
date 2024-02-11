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
        self.insert_state("Generate",1)
        self.insert_state("Next",1)
        self.insert_input_port("start")

        # self.insert_input_port("_ing")
        # self.insert_input_port("Done")
        # self.insert_output_port("pose_next")

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
            # print(f"aaaa\n{self.landmarks_frame[0]}")
            self._cur_state = "Generate"

        # if port == "landmarks":
        #     self.landmarks_frame = msg.retrieve()
        #     self.pose_classify(self.landmarks_frame[0][1])
      
    def output(self): 
         #webcam code
        if self._cur_state == "Generate":
            # 조건 자동삽입
            if self.count + 1 < self.default_count:
                

                
                self._cur_state = "Next" 
            else:
                print("pose simulation Done")
                self.next_step = False
                self._cur_state = "Wait"  
            
        # if self._cur_state == "Next":
        #     msg = SysMessage(self.get_name(), "pose_next")
        #     msg.insert("Next")
        #     return msg
        
            
    def int_trans(self):
        if self._cur_state == "Next":
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
  
    def contrast_angle(self, input_data, default_data):
        self.count += 1

        self.next_step = True

        