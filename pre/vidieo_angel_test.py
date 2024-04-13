import cv2
import mediapipe as mp
import math
import json

class Video_Pose_Angle_Model():
    def __init__(self):
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_pose = mp.solutions.pose
        self.pose_data = self.mp_pose.Pose(static_image_mode=False, min_detection_confidence=0.5, model_complexity=1)
        self.all_landmarks = []  # 리스트로 초기화

    def run(self):
        cap = cv2.VideoCapture("aaaaaaa.mp4")
        frame_rate = int(cap.get(cv2.CAP_PROP_FPS) * 2.5)  # 기존 프레임 속도에 5를 곱합니다.

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                print("비디오 읽기 실패, 비디오 파일이 올바른지 확인하세요.")
                break

            # 처리 전 BGR 이미지를 RGB로 변환
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = self.pose_data.process(image)

            # 각 프레임의 랜드마크 데이터를 딕셔너리로 변환하여 리스트에 저장
            if results.pose_landmarks:
                frame_landmarks = {
                    "landmarks": [
                        {
                            "x": landmark.x,
                            "y": landmark.y,
                            "z": landmark.z,
                            "visibility": landmark.visibility
                        } for landmark in results.pose_landmarks.landmark
                    ]
                }
                self.all_landmarks.append(frame_landmarks)

            # 건너뛸 프레임 수를 설정하여 비디오 속도를 조절
            for _ in range(int(frame_rate / cap.get(cv2.CAP_PROP_FPS)) - 1):
                cap.read()  # 추가 프레임을 읽고 버립니다.

        cap.release()

        # JSON 파일로 랜드마크 데이터 저장
        with open("arm_leg_video.json", 'w') as json_file:
            json.dump(self.all_landmarks, json_file, indent=1)

# 객체 생성 및 실행
video_pose_model = Video_Pose_Angle_Model()
video_pose_model.run()

# import cv2
# import mediapipe as mp
# import math
# import json

# class Video_Pose_Angle_Model():
#     def __init__(self):
#         self.mp_drawing = mp.solutions.drawing_utils
#         self.mp_pose = mp.solutions.pose
#         self.pose_data = self.mp_pose.Pose(static_image_mode=False, min_detection_confidence=0.5, model_complexity=1)
#         self.all_landmarks = []  # 리스트로 초기화

#     def run(self):
#         cap = cv2.VideoCapture("aaaaaaa.mp4")
#         frame_rate = int(cap.get(cv2.CAP_PROP_FPS) * 4)  # 기존 프레임 속도에 1.5를 곱합니다.

#         while cap.isOpened():
#             ret, frame = cap.read()
#             if not ret:
#                 print("비디오 읽기 실패, 비디오 파일이 올바른지 확인하세요.")
#                 break

#             # 처리 전 BGR 이미지를 RGB로 변환
#             image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#             results = self.pose_data.process(image)

#             # # 각 프레임의 랜드마크 데이터를 딕셔너리로 변환하여 리스트에 저장
#             # if results.pose_landmarks:
#             #     frame_landmarks = {
#             #         "landmarks": [
#             #             {
#             #                 "x": landmark.x,
#             #                 "y": landmark.y,
#             #                 "z": landmark.z,
#             #                 "visibility": landmark.visibility
#             #             } for landmark in results.pose_landmarks.landmark
#             #         ]
#             #     }
#             #     self.all_landmarks.append(frame_landmarks)


#             # # 건너뛸 프레임 수를 설정하여 비디오 속도를 조절
#             for _ in range(int(frame_rate / cap.get(cv2.CAP_PROP_FPS)) - 1):
#                 cap.read()  # 추가 프레임을 읽고 버립니다.

#                 # RGB 이미지를 BGR로 다시 변환하여 표시
#             image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

#             if results.pose_landmarks:
#                 self.mp_drawing.draw_landmarks(image, results.pose_landmarks, self.mp_pose.POSE_CONNECTIONS)

#             cv2.imshow("Pose Detection", image)

#             if cv2.waitKey(5) & 0xFF == 27:  # ESC 키를 누르면 종료
#                 break

            

#         cap.release()
#         cv2.destroyAllWindows()

#         # # JSON 파일로 랜드마크 데이터 저장
#         # with open("arm_leg_video.json", 'w') as json_file:
#         #     json.dump(self.all_landmarks, json_file, indent=1)

# # 객체 생성 및 실행
# video_pose_model = Video_Pose_Angle_Model()
# video_pose_model.run()
