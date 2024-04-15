from pyevsim import BehaviorModelExecutor, Infinite, SysMessage
import numpy as np
import math
import matplotlib as plt
import mediapipe as mp
import json
import cv2
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

        elbow_setangle = [30,180]
        shoulder_setangle = [30,150]
        neck_setangle = [45,70]
        hip_setangle = [120,180]
        knee_setangle = [30,180]
        self.all_setangle = [elbow_setangle,shoulder_setangle,neck_setangle,hip_setangle,knee_setangle]

        self.camera = cv2.VideoCapture(0)

        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_pose = mp.solutions.pose
        self.pose_data = self.mp_pose.Pose(static_image_mode=False, min_detection_confidence=0.5, model_complexity=1)

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
            
            # ## 이것까지 받아 올까 고민슨 보류
            # response = requests.get(URL, params={'key': 'value'})
            # if response.status_code == 200:
            #     received_data = response.json()
            #     self.input_save = received_data['input_data']

            # else:
            #     self._cur_state = "Wait"

            ret, self.frame = self.camera.read()
            self.frame = cv2.flip(self.frame, 1)
            self.frame = cv2.resize(self.frame, (640, 480))

            image = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
            image.flags.writeable = False
            results = self.pose_data.process(image)
            # input image의 너비&높이 탐색
            height, width, _ = image.shape
    
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            self.mp_drawing.draw_landmarks(image, results.pose_landmarks, self.mp_pose.POSE_CONNECTIONS)
            # self.input_save = results.pose_landmarks
                    # cv2.imshow('MediaPipe Pose', cv2.flip(image, 1))
                    # if cv2.waitKey(5) & 0xFF == 27:
                    #     break
            
            self.landmarks = []

            # if self.input_save:
            if results.pose_landmarks:
                # for landmark in range(len(self.input_save)):
                for landmark in results.pose_landmarks.landmark:
                    
                    # self.landmarks.append((int(self.input_save[landmark]['X']*640), \
                    #                        int(self.input_save[landmark]['Y']*320), \
                    #                         (self.input_save[landmark]['Z']*640))) 
                    self.landmarks.append((int(landmark.x * 640), int(landmark.y * 320), (landmark.z * 640)))

                Danger_data = self.pose_classify(self.landmarks)

                # cap.release()
        
                self._cur_state = "angle_trans"  
            else:
                self._cur_state = "Generate"
            
     
        if self._cur_state == "angle_trans":
            msg = SysMessage(self.get_name(), "pose_out")
            msg.insert([Danger_data])
            
            return msg
            
            
    def int_trans(self):
        if self._cur_state == "angle_trans":
            self._cur_state = "Generate"
        elif self._cur_state == "Wait":
            self._cur_state = "Wait"
        elif self._cur_state == "Generate":
            self._cur_state = "Generate"
            

    def pose_classify(self,landmarks):

        self.neck = self.shoulder_point(landmarks[self.mp_pose.PoseLandmark.LEFT_SHOULDER.value],landmarks[self.mp_pose.PoseLandmark.RIGHT_SHOULDER.value])
        
        ################# - - 팔꿈치 - - ###################
        #왼쪽 팔꿈치
        left_elbow_angle  = self.calculateAngle(landmarks[self.mp_pose.PoseLandmark.LEFT_SHOULDER.value],
                                        landmarks[self.mp_pose.PoseLandmark.LEFT_ELBOW.value],
                                        landmarks[self.mp_pose.PoseLandmark.LEFT_WRIST.value])
        
        #오른쪽 팔꿈치
        right_elbow_angle = self.calculateAngle(landmarks[self.mp_pose.PoseLandmark.RIGHT_SHOULDER.value],
                                        landmarks[self.mp_pose.PoseLandmark.RIGHT_ELBOW.value],
                                        landmarks[self.mp_pose.PoseLandmark.RIGHT_WRIST.value]) 
        
        elbow_angle = [left_elbow_angle, right_elbow_angle]
        ###################################################
        ################# - - 어깨 - - #####################
        # 왼쪽 어깨
        left_shoulder_angle = self.calculateAngle(landmarks[self.mp_pose.PoseLandmark.LEFT_ELBOW.value],
                                            landmarks[self.mp_pose.PoseLandmark.LEFT_SHOULDER.value],
                                            landmarks[self.mp_pose.PoseLandmark.LEFT_HIP.value])
        # 오른쪽 어깨
        right_shoulder_angle = self.calculateAngle(landmarks[self.mp_pose.PoseLandmark.RIGHT_HIP.value],
                                            landmarks[self.mp_pose.PoseLandmark.RIGHT_SHOULDER.value],
                                            landmarks[self.mp_pose.PoseLandmark.RIGHT_ELBOW.value])
        
        shoulder_angle = [left_shoulder_angle, right_shoulder_angle]
        ####################################################
        ################# - - 목 - - #####################(데이터 형태 확인 후 머리 위치와 어깨 간 중간 점 만들어서 진행해야함)
        # 왼쪽 목
        left_neck_angle = self.calculateAngle(landmarks[self.mp_pose.PoseLandmark.LEFT_SHOULDER.value],
                                            self.neck,
                                            landmarks[self.mp_pose.PoseLandmark.NOSE.value])
        # 오른쪽 목
        right_neck_angle = self.calculateAngle(landmarks[self.mp_pose.PoseLandmark.RIGHT_SHOULDER.value],
                                            self.neck,
                                            landmarks[self.mp_pose.PoseLandmark.NOSE.value])
        
        neck_angle = [left_neck_angle, right_neck_angle]
        ####################################################
        ################# - - 엉덩이(또는 허리) - - #####################(데이터 형태 확인 후 머리 위치와 어깨 간 중간 점 만들어서 진행해야함)
        # 왼쪽 목
        left_hip_angle = self.calculateAngle(landmarks[self.mp_pose.PoseLandmark.LEFT_SHOULDER.value],
                                            landmarks[self.mp_pose.PoseLandmark.LEFT_HIP.value],
                                            landmarks[self.mp_pose.PoseLandmark.LEFT_KNEE.value])
        # 오른쪽 목
        right_hip_angle = self.calculateAngle(landmarks[self.mp_pose.PoseLandmark.RIGHT_SHOULDER.value],
                                            landmarks[self.mp_pose.PoseLandmark.RIGHT_HIP.value],
                                            landmarks[self.mp_pose.PoseLandmark.RIGHT_KNEE.value])
        
        hip_angle = [left_hip_angle, right_hip_angle]
        ####################################################
        ################# - - 왼쪽 무릎 - - ##################
        # 왼쪽 엉덩이, 왼쪽 무릎, 왼쪽 발목 landmark angle 값 계산 
        left_knee_angle = self.calculateAngle(landmarks[self.mp_pose.PoseLandmark.LEFT_HIP.value],
                                        landmarks[self.mp_pose.PoseLandmark.LEFT_KNEE.value],
                                        landmarks[self.mp_pose.PoseLandmark.LEFT_ANKLE.value])

        # 오른쪽 무릎
        right_knee_angle = self.calculateAngle(landmarks[self.mp_pose.PoseLandmark.RIGHT_HIP.value],
                                        landmarks[self.mp_pose.PoseLandmark.RIGHT_KNEE.value],
                                        landmarks[self.mp_pose.PoseLandmark.RIGHT_ANKLE.value])
        
        knee_angle = [left_knee_angle, right_knee_angle]
        #####################################################

        print(neck_angle)
        self.landmarks = []
        # danger_t = []
        # x_y_z_data = []

        # danger_t = self.check_angle([elbow_angle, shoulder_angle, neck_angle, hip_angle, knee_angle])
        
        # if danger_t is None:
        #     pass
        # else:
        #     for name in danger_t:
        #         name,x_y_z = self.get_landmark_indices(name,landmarks)

                        
                # print(name,x_y_z)

        # return x_y_z_data
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
        return angle
    
    def shoulder_point(self, landmark_l_shoulder, landmark_r_shoulder):

        l_shoulder_x, l_shoulder_y, _  = landmark_l_shoulder
        r_shoulder_x, r_shoulder_y, _ = landmark_r_shoulder
        
        # 어깨 중앙 지점의 좌표를 계산합니다.
        shoulder_center_x = (l_shoulder_x + r_shoulder_x) / 2
        shoulder_center_y = (l_shoulder_y + r_shoulder_y) / 2

        return shoulder_center_x,shoulder_center_y,0
    

    def check_angle(self, angle):

        anglist_all = []

        

        for i in range(len(angle)):
            for j in range(len(angle[0])):
                if self.all_setangle[i][0] < angle[i][j] <  self.all_setangle[i][1]:
                    pass
                else:
                    if i == 0:
                        name = "elbow"
                    elif i == 1:
                        name = "shoulder"
                    elif i == 2 :
                        name = "neck"
                    elif i == 3 :
                        name = "hip"
                    elif i == 4 :
                        name = "knee"

                    if j == 0:
                        direction = "L"
                    else:
                        direction = "R"

                    anglist_all.append(f"{direction}_{name}")

        return anglist_all
    

    def get_landmark_indices(self, joint_data, landmarks):
  
        index_map = {
            "L_elbow": [landmarks[self.mp_pose.PoseLandmark.LEFT_SHOULDER.value],
                        landmarks[self.mp_pose.PoseLandmark.LEFT_ELBOW.value],
                        landmarks[self.mp_pose.PoseLandmark.LEFT_WRIST.value]],
            "L_shoulder": [landmarks[self.mp_pose.PoseLandmark.LEFT_HIP.value],
                            landmarks[self.mp_pose.PoseLandmark.LEFT_SHOULDER.value],
                            landmarks[self.mp_pose.PoseLandmark.LEFT_ELBOW.value]],\
            "L_neck": [landmarks[self.mp_pose.PoseLandmark.LEFT_SHOULDER.value],
                        self.neck,
                        landmarks[self.mp_pose.PoseLandmark.NOSE.value]],
            "L_hip": [landmarks[self.mp_pose.PoseLandmark.LEFT_SHOULDER.value],
                        landmarks[self.mp_pose.PoseLandmark.LEFT_HIP.value],
                        landmarks[self.mp_pose.PoseLandmark.LEFT_KNEE.value]],
            "L_knee": [landmarks[self.mp_pose.PoseLandmark.LEFT_HIP.value],
                        landmarks[self.mp_pose.PoseLandmark.LEFT_KNEE.value],
                        landmarks[self.mp_pose.PoseLandmark.LEFT_ANKLE.value]],
            "R_elbow": [landmarks[self.mp_pose.PoseLandmark.RIGHT_SHOULDER.value],
                        landmarks[self.mp_pose.PoseLandmark.RIGHT_ELBOW.value],
                        landmarks[self.mp_pose.PoseLandmark.RIGHT_WRIST.value]],
            "R_shoulder": [landmarks[self.mp_pose.PoseLandmark.RIGHT_HIP.value],
                            landmarks[self.mp_pose.PoseLandmark.RIGHT_SHOULDER.value],
                            landmarks[self.mp_pose.PoseLandmark.RIGHT_ELBOW.value]],\
            "R_neck": [landmarks[self.mp_pose.PoseLandmark.RIGHT_SHOULDER.value],
                        self.neck,
                        landmarks[self.mp_pose.PoseLandmark.NOSE.value]],
            "R_hip": [landmarks[self.mp_pose.PoseLandmark.RIGHT_SHOULDER.value],
                        landmarks[self.mp_pose.PoseLandmark.RIGHT_HIP.value],
                        landmarks[self.mp_pose.PoseLandmark.RIGHT_KNEE.value]],
            "R_knee": [landmarks[self.mp_pose.PoseLandmark.RIGHT_HIP.value],
                        landmarks[self.mp_pose.PoseLandmark.RIGHT_KNEE.value],
                        landmarks[self.mp_pose.PoseLandmark.RIGHT_ANKLE.value]]       

        }

        return joint_data,index_map[f'{joint_data}']
    



 # l_elbow = self.elbow_setangle[0]< elbow_angle[0] <self.elbow_setangle[1]
        # l_shoulder = self.shoulder_setangle[0]< shoulder_angle[0] <self.shoulder_setangle[1]
        # l_neck = self.neck_setangle[0]< neck_angle[0] <self.neck_setangle[1]
        # l_hip = self.hip_setangle[0]< self.hip_angle[0] <self.hip_setangle[1]
        # l_knee = self.knee_setangle[0]< self.knee_angle[0] <self.knee_setangle[1]

        # r_elbow = self.elbow_setangle[0]< self.elbow_angle[1] <self.elbow_setangle[1]
        # r_shoulder = self.shoulder_setangle[0]< self.shoulder_angle[1] <self.shoulder_setangle[1]
        # r_neck = self.neck_setangle[0]< self.neck_angle[1] <self.neck_setangle[1]
        # r_hip = self.hip_setangle[0]< self.hip_angle[1] <self.hip_setangle[1]
        # r_knee = self.knee_setangle[0]< self.knee_angle[1] <self.knee_setangle[1]