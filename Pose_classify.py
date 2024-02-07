from pyevsim import BehaviorModelExecutor, Infinite, SysMessage
import numpy as np
import math
import matplotlib as plt


class Posture_Classify_Model(BehaviorModelExecutor):
    def __init__(self, instance_time, destruct_time, name, engine_name):
        BehaviorModelExecutor.__init__(self, instance_time, destruct_time, name, engine_name)
        
        self.init_state("Wait")
        self.insert_state("Wait", Infinite)
        self.insert_state("Generate",1)
        self.insert_state("Next",1)
        self.insert_input_port("start")
        self.insert_input_port("_ing")
        self.insert_input_port("Done")
        self.insert_output_port("pose_next")
        self.insert_output_port("pose_done")
       
        self.landmarks = []

        self.next_step = True
        
    def ext_trans(self, port, msg):
        
        if port == "start":
            self._cur_state = "Generate"

        if port == "_ing":
            self._cur_state = "Generate"

        if port == "Done":
            self._cur_state = "Generate"

        # if port == "landmarks":
        #     self.landmarks_frame = msg.retrieve()
        #     self.pose_classify(self.landmarks_frame[0][1])
      
    def output(self): 
         #webcam code
        if self._cur_state == "Generate":
            # 조건 자동삽입
            if 30 < 60:
                self.next_step = True
                self._cur_state = "Next" 
            else:
                self.next_step = False
                self._cur_state = "Wait"  
            
        if self._cur_state == "Next":
            msg = SysMessage(self.get_name(), "pose_out")
            msg.insert("Next")
            return msg
            
            
    def int_trans(self):
        if self._cur_state == "Next":
            self._cur_state = "Generate"
        elif self._cur_state == "Wait":
            self._cur_state = "Generate"
            
    
                