from pyevsim import BehaviorModelExecutor, Infinite, SysMessage
import numpy as np
import math
import matplotlib as plt
import mediapipe as mp
import json
import requests

class Posture_Check_Model(BehaviorModelExecutor):
    input_save = ''
    def __init__(self, instance_time, destruct_time, name, engine_name):
        BehaviorModelExecutor.__init__(self, instance_time, destruct_time, name, engine_name)
        
        self.init_state("Wait")
        self.insert_state("Wait", Infinite)
        self.insert_state("Generate",0)

        self.insert_input_port("start")


        self.insert_output_port("pose_out")

        self.mp_pose = mp.solutions.pose
        # self.pose_data = self.mp_pose.Pose(static_image_mode=False, min_detection_confidence=0.5, model_complexity=1)

        self.landmarks = []
        self.count = 0
        
    def ext_trans(self, port, msg):
        
        if port == "start":
            self._cur_state = "Generate"

        if port == "-ing": #실패
            # print("classify -> check")
            self.count = msg.retrieve()[0][1]
            self._cur_state = "Generate"
        if port == "next": #성공
           
            self.count = msg.retrieve()[0][1]
            self._cur_state = "Generate"

      
    def output(self): 
         #webcam code
        if self._cur_state == "Generate":
            
            ## 이것까지 받아 올까 고민슨 보류
            response = requests.get(URL, params={'key': 'value'})
            if response.status_code == 200:
                received_data = response.json()
                self.input_save = received_data['input_data']

            else:
                self._cur_state = "Wait"
            

            if self.input_save:
                for landmark in range(len(self.input_save)):
                    
                    self.landmarks.append((int(self.input_save[landmark]['X']*640), \
                                           int(self.input_save[landmark]['Y']*320), \
                                            (self.input_save[landmark]['Z']*640))) 

                elbow,shoulder,neck,hip,knee = self.pose_classify(self.landmarks)
        
                self._cur_state = "angle_trans"  
            else:
                self._cur_state = "Generate"
            
     
        if self._cur_state == "angle_trans":
            msg = SysMessage(self.get_name(), "pose_out")
            msg.insert([elbow, shoulder, neck, hip,knee])
            
            return msg
            
            
    def int_trans(self):
        if self._cur_state == "angle_trans":
            self._cur_state = "Generate"
        elif self._cur_state == "Wait":
            self._cur_state = "Wait"
        elif self._cur_state == "Generate":
            self._cur_state = "Generate"
            

    def pose_classify(self,landmarks):

        NECK = self.shoulder_point(landmarks[self.mp_pose.PoseLandmark.LEFT_SHOULDER.value],landmarks[self.mp_pose.PoseLandmark.RIGHT_SHOULDER.value])
        
        ################# - - 팔꿈치 - - ###################
        #왼쪽 팔꿈치
        left_elbow_angle, l_elbow_one_xy, l_elbow_two_xy, l_elbow_three_xy  = self.calculateAngle(landmarks[self.mp_pose.PoseLandmark.LEFT_SHOULDER.value],
                                        landmarks[self.mp_pose.PoseLandmark.LEFT_ELBOW.value],
                                        landmarks[self.mp_pose.PoseLandmark.LEFT_WRIST.value])
        
        #오른쪽 팔꿈치
        right_elbow_angle, r_elbow_one_xy, r_elbow_two_xy, r_elbow_three_xy = self.calculateAngle(landmarks[self.mp_pose.PoseLandmark.RIGHT_SHOULDER.value],
                                        landmarks[self.mp_pose.PoseLandmark.RIGHT_ELBOW.value],
                                        landmarks[self.mp_pose.PoseLandmark.RIGHT_WRIST.value]) 
        ###################################################
        ################# - - 어깨 - - #####################
        # 왼쪽 어깨
        left_shoulder_angle, l_shoulder_one_xy, l_shoulder_two_xy, l_shoulder_three_xy = self.calculateAngle(landmarks[self.mp_pose.PoseLandmark.LEFT_ELBOW.value],
                                            landmarks[self.mp_pose.PoseLandmark.LEFT_SHOULDER.value],
                                            landmarks[self.mp_pose.PoseLandmark.LEFT_HIP.value])
        # 오른쪽 어깨
        right_shoulder_angle, r_shoulder_one_xy, r_shoulder_two_xy, r_shoulder_three_xy = self.calculateAngle(landmarks[self.mp_pose.PoseLandmark.RIGHT_HIP.value],
                                            landmarks[self.mp_pose.PoseLandmark.RIGHT_SHOULDER.value],
                                            landmarks[self.mp_pose.PoseLandmark.RIGHT_ELBOW.value])
        ####################################################
        ################# - - 목 - - #####################(데이터 형태 확인 후 머리 위치와 어깨 간 중간 점 만들어서 진행해야함)
        # 왼쪽 목
        left_neck_angle, l_neck_one_xy, l_neck_two_xy, l_neck_three_xy = self.calculateAngle(landmarks[self.mp_pose.PoseLandmark.LEFT_SHOULDER.value],
                                            NECK,
                                            landmarks[self.mp_pose.PoseLandmark.NOSE.value])
        # 오른쪽 목
        right_neck_angle, r_neck_one_xy, r_neck_two_xy, r_neck_three_xy = self.calculateAngle(landmarks[self.mp_pose.PoseLandmark.RIGHT_SHOULDER.value],
                                            NECK,
                                            landmarks[self.mp_pose.PoseLandmark.NOSE.value])
        ####################################################
        ################# - - 엉덩이(또는 허리) - - #####################(데이터 형태 확인 후 머리 위치와 어깨 간 중간 점 만들어서 진행해야함)
        # 왼쪽 목
        left_hip_angle, l_hip_one_xy, l_hip_two_xy, l_hip_three_xy = self.calculateAngle(landmarks[self.mp_pose.PoseLandmark.LEFT_SHOULDER.value],
                                            landmarks[self.mp_pose.PoseLandmark.LEFT_HIP.value],
                                            landmarks[self.mp_pose.PoseLandmark.LEFT_KNEE.value])
        # 오른쪽 목
        right_hip_angle, r_hip_one_xy, r_hip_two_xy, r_hip_three_xy = self.calculateAngle(landmarks[self.mp_pose.PoseLandmark.RIGHT_SHOULDER.value],
                                            landmarks[self.mp_pose.PoseLandmark.RIGHT_HIP.value],
                                            landmarks[self.mp_pose.PoseLandmark.RIGHT_KNEE.value])
        ####################################################
        ################# - - 왼쪽 무릎 - - ##################
        # 왼쪽 엉덩이, 왼쪽 무릎, 왼쪽 발목 landmark angle 값 계산 
        left_knee_angle, l_knee_one_xy, l_knee_two_xy, l_knee_three_xy = self.calculateAngle(landmarks[self.mp_pose.PoseLandmark.LEFT_HIP.value],
                                        landmarks[self.mp_pose.PoseLandmark.LEFT_KNEE.value],
                                        landmarks[self.mp_pose.PoseLandmark.LEFT_ANKLE.value])

        # 오른쪽 무릎
        right_knee_angle, r_knee_one_xy, r_knee_two_xy, r_knee_three_xy = self.calculateAngle(landmarks[self.mp_pose.PoseLandmark.RIGHT_HIP.value],
                                        landmarks[self.mp_pose.PoseLandmark.RIGHT_KNEE.value],
                                        landmarks[self.mp_pose.PoseLandmark.RIGHT_ANKLE.value])
        #####################################################
        self.landmarks = []
        
        return [[left_elbow_angle,[l_elbow_one_xy, l_elbow_two_xy, l_elbow_three_xy]], [right_elbow_angle,[r_elbow_one_xy, r_elbow_two_xy, r_elbow_three_xy]]],\
            [[left_shoulder_angle,[l_shoulder_one_xy, l_shoulder_two_xy, l_shoulder_three_xy]], [right_shoulder_angle,[r_shoulder_one_xy, r_shoulder_two_xy, r_shoulder_three_xy]]],\
                [[left_neck_angle,[l_neck_one_xy, l_neck_two_xy, l_neck_three_xy]], [right_neck_angle,[r_neck_one_xy, r_neck_two_xy, r_neck_three_xy]]],\
                    [[left_hip_angle,[l_hip_one_xy, l_hip_two_xy, l_hip_three_xy]], [right_hip_angle,[r_hip_one_xy, r_hip_two_xy, r_hip_three_xy]]],\
                        [[left_knee_angle,[l_knee_one_xy, l_knee_two_xy, l_knee_three_xy]], [right_knee_angle,[r_knee_one_xy, r_knee_two_xy, r_knee_three_xy]]]

     # 앵글 계산 함수
    def calculateAngle(self, landmark1, landmark2, landmark3):

        # Get the required landmarks coordinates.
        x1, y1, _ = landmark1
        x2, y2, _ = landmark2
        x3, y3, _ = landmark3

        # Calculate the angle between the three points
        angle = math.degrees(math.atan2(y3 - y2, x3 - x2) - math.atan2(y1 - y2, x1 - x2))
        
        # angle_degree = angle % 360
        # # Check if the angle is less than zero.
        if angle < 0:

            # Add 360 to the found angle.
            angle += 360
        
        # Return the calculated angle.
        return angle, [x1, y1, _], [x2, y2, _], [x3, y3, _]
    
    def shoulder_point(self, landmark_l_shoulder, landmark_r_shoulder):

        l_shoulder_x, l_shoulder_y, _  = landmark_l_shoulder
        r_shoulder_x, r_shoulder_y, _ = landmark_r_shoulder
        
        # 어깨 중앙 지점의 좌표를 계산합니다.
        shoulder_center_x = (l_shoulder_x + r_shoulder_x) / 2
        shoulder_center_y = (l_shoulder_y + r_shoulder_y) / 2

        return shoulder_center_x,shoulder_center_y,0