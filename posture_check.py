from pyevsim import BehaviorModelExecutor, Infinite, SysMessage
import numpy as np
import math
import matplotlib as plt
import mediapipe as mp



class Posture_Check_Model(BehaviorModelExecutor):
    def __init__(self, instance_time, destruct_time, name, engine_name, data):
        BehaviorModelExecutor.__init__(self, instance_time, destruct_time, name, engine_name)
        
        self.init_state("Wait")

        self.insert_state("Wait", Infinite)
        self.insert_state("Generate",1)

        self.insert_state("angle_trans")

        self.insert_input_port("start")
        self.insert_input_port("next")
        self.insert_input_port("-ing")

        self.insert_output_port("pose_out")
        
        self.data = data
        # self.camera = cv2.VideoCapture(0)

        # frame_Data to Pose Data(임시_pose데이터 수집기 mediapipe)
        # self.mp_drawing = mp.solutions.drawing_utils
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
            # 임시 스켈레톤 변환 코드(해당 부분 Alphapose로 대체 예정) -> (mediapipe로 유지하지만 시뮬레이션 내에서는 사라짐)
            # ret, self.frame = self.camera.read()
            
            # # input image의 너비&높이 탐색
            # height, width, _ = self.frame.shape
            # results = self.pose_data.process(cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB))

            # landmark가 감지 되었는지 확인
            if self.data:
                # landmark 그리기
                # self.mp_drawing.draw_landmarks(image=self.frame, landmark_list=results.pose_landmarks, connections=self.mp_pose.POSE_CONNECTIONS)
                # 감지된 landmark 반복
                for landmark in range(len(self.data)):
                    
                    # landmark를 list에 추가하기
                    self.landmarks.append((int(self.data[landmark]['X']), int(self.data[landmark]['Y']), (self.data[landmark]['Z'])))
            
                # 요기까지가 landmarks에 대한 수집 부분.
                elbow,shoulder,knee = self.pose_classify(self.landmarks)
                
                self._cur_state = "angle_trans"  
            else:
                self._cur_state = "Generate"
            # cv2.imshow("mobile image", self.frame)
            # cv2.waitKey(1)  
                
            # print(f"elbow {elbow}\nshoulder {shoulder}\nknee {knee}")
            
     
        if self._cur_state == "angle_trans":
            msg = SysMessage(self.get_name(), "pose_out")
            msg.insert([self.count, [elbow, shoulder, knee]])
            
            return msg
            
            
    def int_trans(self):
        if self._cur_state == "angle_trans":
            self._cur_state = "Generate"
        elif self._cur_state == "Wait":
            self._cur_state = "Wait"
        elif self._cur_state == "Generate":
            self._cur_state = "Generate"
            
            
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
        
        self.landmarks = []
        
        return [left_elbow_angle, right_elbow_angle],[left_shoulder_angle, right_shoulder_angle],[left_knee_angle, right_knee_angle]

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
    
