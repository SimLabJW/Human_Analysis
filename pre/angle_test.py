import cv2
import numpy as np
import mediapipe as mp
import math
import json
from config import *

class Image_Pose_Angle_Model():
    def __init__(self):
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_pose = mp.solutions.pose
        self.pose_data = self.mp_pose.Pose(static_image_mode=False, min_detection_confidence=0.5, model_complexity=1)
        self.pose_angle = {}
      
    def output(self): 
        #code
        self.landmark_zip = []
      
        self.mp_drawing = mp.solutions.drawing_utils

        
        self.image = cv2.imread("arm_leg_1.png")
        
        image_height, image_width, _ = self.image.shape
        # 처리 전 BGR 이미지를 RGB로 변환합니다.
        results = self.pose_data.process(cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB))


        if results.pose_landmarks:
            self.mp_drawing.draw_landmarks(image=self.image, landmark_list=results.pose_landmarks, connections=self.mp_pose.POSE_CONNECTIONS)
            
                # 감지된 landmark 반복
            for landmark in results.pose_landmarks.landmark:
                # landmark를 list에 추가하기
                self.landmark_zip.append((int(landmark.x * image_width), int(landmark.y * image_height), (landmark.z * image_width)))

            # for landmark in results.pose_landmarks.landmark:
            #     # landmark를 list에 추가하기
            #     self.landmark_zip.append((int(landmark.x), int(landmark.y), (landmark.z)))

                # 요기까지가 landmarks에 대한 수집 부분.
          
            data =  self.pose_classify(self.landmark_zip)

                
        cv2.imshow("mobile image", self.image)
        cv2.waitKey() 
            # JSON 파일로 저장
            # json_file_path = ANGLE_JSON
            # with open(json_file_path, 'w') as json_file:
            #     json.dump(self.pose_angle, json_file, indent=1)
                    # print(f"key {key}\nelbow {elbow}\nshoulder {shoulder}\nknee {knee}")


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

        print(self.neck)
        print(f"left {landmarks[self.mp_pose.PoseLandmark.LEFT_SHOULDER.value]}")
        
        print(f"right {landmarks[self.mp_pose.PoseLandmark.RIGHT_SHOULDER.value]}")
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
    
Image_Pose_Angle_Model().output()