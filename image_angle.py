import cv2
import mediapipe as mp
import numpy as np
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose

# 이미지 파일의 경우 이것을 사용하세요.:
IMAGE_FILES = "./Pose_zip/"
BG_COLOR = (192, 192, 192)  # 회색
with mp_pose.Pose(
        static_image_mode=True,
        model_complexity=2,
        enable_segmentation=True,
        min_detection_confidence=0.5) as pose:
    for idx, file in enumerate(IMAGE_FILES):
        image = cv2.imread(file)
        image_height, image_width, _ = image.shape
        # 처리 전 BGR 이미지를 RGB로 변환합니다.
        results = pose.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

        if not results.pose_landmarks:
            continue

        annotated_image = image.copy()
        # 이미지를 분할합니다.
        # 경계 주변의 분할을 개선하려면 "image"가 있는
        # "results.segmentation_mask"에 공동 양방향 필터를 적용하는 것이 좋습니다.
        condition = np.stack((results.segmentation_mask,) * 3, axis=-1) > 0.1
        bg_image = np.zeros(image.shape, dtype=np.uint8)
        bg_image[:] = BG_COLOR
        annotated_image = np.where(condition, annotated_image, bg_image)

        # 이미지 위에 포즈 랜드마크를 그립니다.
        mp_drawing.draw_landmarks(
            annotated_image,
            results.pose_landmarks,
            mp_pose.POSE_CONNECTIONS,
            landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())

        # 이미지를 출력합니다.
        cv2.imshow('Annotated Image', annotated_image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
