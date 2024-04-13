from pyevsim import BehaviorModelExecutor, SystemSimulator, Infinite
import mediapipe as mp
import json
import numpy as np
from mediapipe.framework.formats import landmark_pb2

class Visual_Model(BehaviorModelExecutor):
    def __init__(self, instance_time, destruct_time, name, engine_name):
        BehaviorModelExecutor.__init__(self, instance_time, destruct_time, name, engine_name)

        self.init_state("Wait")
        self.insert_state("Wait", Infinite)
        self.insert_state("Generate",1)

        self.insert_input_port("start")

        self.json_path = "arm_leg_video.json"
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_pose = mp.solutions.pose
        self.pose_connections = self.mp_pose.POSE_CONNECTIONS

    def ext_trans(self, port, msg):
        if port == "start":
            self._cur_state = "Generate"

        
    def output(self): 

        if self._cur_state == "Generate":
            self.display_skeleton()

            
    def int_trans(self):
        if self._cur_state == "Generate":
            self._cur_state = "Generate"

    def display_skeleton(self):
        # JSON 파일 로드
        with open(self.json_path, 'r') as json_file:
            all_landmarks = json.load(json_file)

        for frame_data in all_landmarks:
      
            landmarks = frame_data['landmarks']
            pose_landmarks = landmark_pb2.NormalizedLandmarkList()  # 수정된 부분
            for landmark in landmarks:
                new_landmark = pose_landmarks.landmark.add()
                new_landmark.x = landmark['x']
                new_landmark.y = landmark['y']
                new_landmark.z = landmark['z']
                new_landmark.visibility = landmark.get('visibility', 0)
                
             ###요기서 들고가기로 나랑 약속
            print(pose_landmarks)# 수정된 부분
            




