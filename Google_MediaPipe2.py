import cv2
import mediapipe as mp
import math

print(mp.__file__)

L_shoulder = (23, 11, 13)
L_KNEE = (23, 25, 27)
R_shoulder = (24, 12, 14)
R_KNEE = (24, 26, 28)

bodys = [L_ELBOW, R_ELBOW, L_KNEE, R_KNEE]

# MediaPipe의 Pose 모델 초기화
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()
mp_drawing = mp.solutions.drawing_utils

def calculate_angle(point1, point2, point3):
    # 좌표 추출
    x1, y1 = point1 
    x2, y2 = point2
    x3, y3 = point3
    
    # 벡터 사이의 각도 계산
    angle = math.degrees(math.atan2(y3 - y2, x3 - x2) - math.atan2(y1 - y2, x1 - x2))
    angle = abs(angle) # 각도를 절댓값으로 변환
    if angle > 180:
        angle = 360 - angle
    return angle

# 비디오 파일 열기
try:
    #cap = cv2.VideoCapture('sample3.mp4')
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
except Exception as e:
    print('Cam Error : ', e)
else:
    width = 1024
    height = 768

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # 프레임 리사이즈
        frame = cv2.resize(frame, (width, height))

        # 이미지를 RGB로 변환 (MediaPipe는 RGB 이미지를 사용)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
        # Pose 모델을 통해 골격 추출
        result = pose.process(rgb_frame)

        # 원본 프레임에 골격 표시
        if result.pose_landmarks:
            mp_drawing.draw_landmarks(frame, result.pose_landmarks, mp_pose.POSE_CONNECTIONS)
            
            # 좌표 추출
            landmarks = result.pose_landmarks.landmark
            
            for body in bodys:
                pts = []
                for i in range(len(body)):
                    pt = (landmarks[body[i]].x * frame.shape[1], landmarks[body[i]].y * frame.shape[0])                     
                    pts.append(pt)
            
                # 각도 계산 (예: 어깨-엉덩이-무릎 각도)
                angle = calculate_angle(pts[0], pts[1], pts[2])
            
                # 각도 화면에 표시
                cv2.putText(frame, str(int(angle)), 
                            (int(pts[1][0]), int(pts[1][1])), 
                            cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 200, 0), 2, cv2.LINE_AA)

        # 결과 프레임을 화면에 출력
        cv2.imshow('Cyclist Pose Detection v 1.0 (Ocean Coding School), Exit : q', frame)

        if cv2.waitKey(1) & 0xFF == ord('q') :
            break

cap.release()
cv2.destroyAllWindows()
