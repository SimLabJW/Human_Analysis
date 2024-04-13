import cv2
import mediapipe as mp
import json
import numpy as np
from mediapipe.framework.formats import landmark_pb2  # 이 줄을 추가

class Skeleton_Display():
    def __init__(self, json_path):
        self.json_path = json_path
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_pose = mp.solutions.pose
        self.pose_connections = self.mp_pose.POSE_CONNECTIONS

    def display_skeleton(self):
        # JSON 파일 로드
        with open(self.json_path, 'r') as json_file:
            all_landmarks = json.load(json_file)

        # 윈도우 생성
        cv2.namedWindow("Skeleton Display", cv2.WINDOW_NORMAL)
        cv2.resizeWindow("Skeleton Display", 640, 480)

        for frame_data in all_landmarks:
            # 빈 이미지/프레임 생성
            image = np.zeros((480, 640, 3), dtype=np.uint8)

            # 랜드마크 데이터를 이미지에 그리기
            landmarks = frame_data['landmarks']
            pose_landmarks = landmark_pb2.NormalizedLandmarkList()  # 수정된 부분
            for landmark in landmarks:
                new_landmark = pose_landmarks.landmark.add()
                new_landmark.x = landmark['x']
                new_landmark.y = landmark['y']
                new_landmark.z = landmark['z']
                new_landmark.visibility = landmark.get('visibility', 0)

            # 스켈레톤 그리기
            self.mp_drawing.draw_landmarks(image, pose_landmarks, self.pose_connections)

            # 생성된 이미지를 윈도우에 출력
            cv2.imshow("Skeleton Display", image)
            if cv2.waitKey(int(1000/30)) & 0xFF == 27:  # ESC 키를 누르면 종료
                break

        # 자원 해제
        cv2.destroyAllWindows()

# 객체 생성 및 실행
skeleton_display = Skeleton_Display('arm_leg_video.json')
skeleton_display.display_skeleton()
