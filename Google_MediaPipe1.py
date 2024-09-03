import cv2
import mediapipe as mp

# MediaPipe의 Pose 모델 초기화
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()
mp_drawing = mp.solutions.drawing_utils

# 비디오 파일 열기
#cap = cv2.VideoCapture('sample1.mp4')
try:
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
except Exception as e:
    print('Cam Error : ', e)
else:

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # 이미지를 RGB로 변환 (MediaPipe는 RGB 이미지를 사용)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
        # Pose 모델을 통해 골격 추출
        result = pose.process(rgb_frame)

        # 원본 프레임에 골격 표시
        if result.pose_landmarks:
            mp_drawing.draw_landmarks(frame, result.pose_landmarks, mp_pose.POSE_CONNECTIONS)
    
        # 결과 프레임을 화면에 출력
        cv2.imshow('Cyclist Pose Detection', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()