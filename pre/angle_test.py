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

        
        image = cv2.imread("arm_leg_1.png")
        
        image_height, image_width, _ = image.shape
        # 처리 전 BGR 이미지를 RGB로 변환합니다.
        results = self.pose_data.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))


        if results.pose_landmarks:
            self.mp_drawing.draw_landmarks(image=image, landmark_list=results.pose_landmarks, connections=self.mp_pose.POSE_CONNECTIONS)
            
       
            print(results.pose_landmarks.landmark)
                # 감지된 landmark 반복
            for landmark in results.pose_landmarks.landmark:
                # landmark를 list에 추가하기
                self.landmark_zip.append((int(landmark.x * image_width), int(landmark.y * image_height), (landmark.z * image_width)))

            # for landmark in results.pose_landmarks.landmark:
            #     # landmark를 list에 추가하기
            #     self.landmark_zip.append((int(landmark.x), int(landmark.y), (landmark.z)))

                # 요기까지가 landmarks에 대한 수집 부분.
          
            elbow,shoulder,knee =  self.pose_classify(self.landmark_zip)
            print(f"elbow {elbow}\nshoulder {shoulder}\nknee {knee}")
                
        cv2.imshow("mobile image", image)
        cv2.waitKey() 
            # JSON 파일로 저장
            # json_file_path = ANGLE_JSON
            # with open(json_file_path, 'w') as json_file:
            #     json.dump(self.pose_angle, json_file, indent=1)
                    # print(f"key {key}\nelbow {elbow}\nshoulder {shoulder}\nknee {knee}")


    def pose_classify(self,landmarks):
        
        # 각도의 여러가지 방향성 고려가 필요. 머리부터 발끝까지 이룰 수 있는 모든 각도들이 더 존재함.

        # 11번, 13번, 15번 landmark 
        # 왼쪽 어깨, 왼쪽 팔꿈치, 왼쪽 손목 landmark angle 값 계산 
        left_elbow_angle = self.calculateAngle(landmarks[self.mp_pose.PoseLandmark.LEFT_SHOULDER.value],
                                        landmarks[self.mp_pose.PoseLandmark.LEFT_ELBOW.value],
                                        landmarks[self.mp_pose.PoseLandmark.LEFT_WRIST.value])
        
        
        # 12번, 14번, 16번 landmark 
        # 오른쪽 어깨, 오른쪽 팔꿈치, 오른쪽 손목 landmark angle 값 계산 
        right_elbow_angle = self.calculateAngle(landmarks[self.mp_pose.PoseLandmark.RIGHT_SHOULDER.value],
                                        landmarks[self.mp_pose.PoseLandmark.RIGHT_ELBOW.value],
                                        landmarks[self.mp_pose.PoseLandmark.RIGHT_WRIST.value]) 
        
        
        # 13번, 15번, 23번 landmark 
        # 왼쪽 팔꿈치, 왼쪽 어깨, 왼쪽 엉덩이, landmark angle 값 계산 
        left_shoulder_angle = self.calculateAngle(landmarks[self.mp_pose.PoseLandmark.LEFT_ELBOW.value],
                                            landmarks[self.mp_pose.PoseLandmark.LEFT_SHOULDER.value],
                                            landmarks[self.mp_pose.PoseLandmark.LEFT_HIP.value])
        # print(f'left shoulder engle : {left_shoulder_angle}')
        # 12번, 14번, 24번 landmark 
        # 오른쪽 팔꿈치, 오른쪽 어깨, 오른쪽 엉덩이 landmark angle 값 계산  
        right_shoulder_angle = self.calculateAngle(landmarks[self.mp_pose.PoseLandmark.RIGHT_HIP.value],
                                            landmarks[self.mp_pose.PoseLandmark.RIGHT_SHOULDER.value],
                                            landmarks[self.mp_pose.PoseLandmark.RIGHT_ELBOW.value])
        # print(f'right shoulder engle : {right_shoulder_angle}')
        # 23번, 25번, 27번 landmark 
        # 왼쪽 엉덩이, 왼쪽 무릎, 왼쪽 발목 landmark angle 값 계산 
        left_knee_angle = self.calculateAngle(landmarks[self.mp_pose.PoseLandmark.LEFT_HIP.value],
                                        landmarks[self.mp_pose.PoseLandmark.LEFT_KNEE.value],
                                        landmarks[self.mp_pose.PoseLandmark.LEFT_ANKLE.value])

        # 24번, 26번, 28번 landmark 
        # 오른쪽 엉덩이, 오른쪽 무릎, 오른쪽 발목  landmark angle 값 계산 
        right_knee_angle = self.calculateAngle(landmarks[self.mp_pose.PoseLandmark.RIGHT_HIP.value],
                                        landmarks[self.mp_pose.PoseLandmark.RIGHT_KNEE.value],
                                        landmarks[self.mp_pose.PoseLandmark.RIGHT_ANKLE.value])
        
        self. landmark_zip = []
        return [left_elbow_angle, right_elbow_angle],[left_shoulder_angle, right_shoulder_angle], [left_knee_angle, right_knee_angle]
        
        # self.landmarks = []

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
    
Image_Pose_Angle_Model().output()