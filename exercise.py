import cv2
import numpy as np
import mediapipe as mp

def exercise(name, number):
    if name == "SQUAT":
        return squat(number)
    elif name == "LUNGE":
        return lunge(number)
    elif name == "PUSH_UP":
        return push_up(number)
def lunge(number):
    mp_pose = mp.solutions.pose
    mp_hands = mp.solutions.hands       #정확도             #반응성
    pose = mp_pose.Pose(min_detection_confidence=0.8, min_tracking_confidence=0.8)
    hand = mp_hands.Hands(max_num_hands=1,min_detection_confidence=0.5, min_tracking_confidence=0.5)
    mp_drawing = mp.solutions.drawing_utils             #랜드마크를 동영상에 표시해주는 코드

    # 런지 개수와 상태 변수
    lunge_count = 0
    is_lunging = False
    is_lunge_detecting = False  # 손 모양 감지 상태
    hand_detected=False

    # 비디오 스트림 열기
    camera = cv2.VideoCapture(0)

    while camera.isOpened():
        ret, frame = camera.read()
        if not ret:
            break

        # BGR 이미지를 RGB로 변환
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False

        # MediaPipe로 포즈와 손 분석
        pose_results = pose.process(image)      #mediapipe에서 사람의 포즈를 분석하기 위해서 사용
        hand_results = hand.process(image)      #mediapipe에서 사람의 손을 분석하기 위해서 사용

        # RGB 이미지를 다시 BGR로 변환
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        # 손 모양 확인 (보자기 모양 감지)
        if hand_detected==False:
            hand_detected=hand_detecting(hand_results,image)
        if hand_detected:
            is_lunge_detecting =True


        # 런지 감지
        if is_lunge_detecting and pose_results.pose_landmarks:
            landmarks = pose_results.pose_landmarks.landmark        #관절의 좌표를 보여줌
            try:
                # 왼쪽 다리 좌표 (엉덩이, 무릎, 발목)
                left_hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x * frame.shape[1],
                            landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y * frame.shape[0]]
                left_knee = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x * frame.shape[1],
                             landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y * frame.shape[0]]
                left_ankle = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x * frame.shape[1],
                              landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y * frame.shape[0]]

                # 오른쪽 다리 좌표 (엉덩이, 무릎, 발목)
                right_hip = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x * frame.shape[1],
                             landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y * frame.shape[0]]
                right_knee = [landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x * frame.shape[1],
                              landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y * frame.shape[0]]
                right_ankle = [landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].x * frame.shape[1],
                               landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].y * frame.shape[0]]

                # 각도 계산
                left_angle = calculate_angle(left_hip, left_knee, left_ankle)
                right_angle = calculate_angle(right_hip, right_knee, right_ankle)

                # 런지 판정: 두 무릎 모두 앉은 상태 -> 일어난 상태
                if left_angle < 110 and 80 < right_angle < 100:  # 앉은 상태
                    if not is_lunging:
                        is_lunging = True
                elif right_angle <110 and 80 < left_angle < 100:
                    if not is_lunging:
                        is_lunging = True
                elif left_angle > 160 and right_angle > 160:  # 일어난 상태
                    if is_lunging:
                        is_lunging = False
                        lunge_count += 1

                # 성공 메시지
                if lunge_count == number:
                    lunge_completed = True
                    break

            except IndexError:
                pass
        if hand_detected ==True:
            cv2.putText(image, "Measuring!", (20, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        # 런지 개수 표시 (항상 표시)
        cv2.putText(image, f"Count: {lunge_count} / {number}", (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        # 랜드마크 시각화
        if pose_results.pose_landmarks:
            mp_drawing.draw_landmarks(image, pose_results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
        if hand_results.multi_hand_landmarks:
            for hand_landmarks in hand_results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

        cv2.imshow("Lunge Counter", image)

        if cv2.waitKey(1) & 0xFF == ord('q'):  # 'q'를 눌러 종료
            lunge_completed = False
            break

    camera.release()
    cv2.destroyAllWindows()
    return lunge_completed
    
# MediaPipe 포즈 및 손 설정
def squat(number):
    mp_pose = mp.solutions.pose
    mp_hands = mp.solutions.hands       #정확도             #반응성
    pose = mp_pose.Pose(min_detection_confidence=0.8, min_tracking_confidence=0.8)
    hand = mp_hands.Hands(max_num_hands=1,min_detection_confidence=0.5, min_tracking_confidence=0.5)
    mp_drawing = mp.solutions.drawing_utils             #랜드마크를 동영상에 표시해주는 코드

    # 스쿼트 개수와 상태 변수
    squat_count = 0
    is_squatting = False
    is_squat_detecting = False  # 손 모양 감지 상태
    hand_detected=False

    # 비디오 스트림 열기
    camera = cv2.VideoCapture(0)

    while camera.isOpened():
        ret, frame = camera.read()
        if not ret:
            break

        # BGR 이미지를 RGB로 변환
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False

        # MediaPipe로 포즈와 손 분석
        pose_results = pose.process(image)      #mediapipe에서 사람의 포즈를 분석하기 위해서 사용
        hand_results = hand.process(image)      #mediapipe에서 사람의 손을 분석하기 위해서 사용

        # RGB 이미지를 다시 BGR로 변환
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        # 손 모양 확인 (보자기 모양 감지)
        if hand_detected==False:
            hand_detected=hand_detecting(hand_results,image)
            print(f"hand_detected after: {hand_detected}")
        if hand_detected:
            is_squat_detecting =True


        # 스쿼트 감지
        if is_squat_detecting and pose_results.pose_landmarks:
            landmarks = pose_results.pose_landmarks.landmark        #관절의 좌표를 보여줌
            try:
                # 왼쪽 다리 좌표 (엉덩이, 무릎, 발목)
                left_hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x * frame.shape[1],
                            landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y * frame.shape[0]]
                left_knee = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x * frame.shape[1],
                             landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y * frame.shape[0]]
                left_ankle = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x * frame.shape[1],
                              landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y * frame.shape[0]]

                # 오른쪽 다리 좌표 (엉덩이, 무릎, 발목)
                right_hip = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x * frame.shape[1],
                             landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y * frame.shape[0]]
                right_knee = [landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x * frame.shape[1],
                              landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y * frame.shape[0]]
                right_ankle = [landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].x * frame.shape[1],
                               landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].y * frame.shape[0]]

                # 각도 계산
                left_angle = calculate_angle(left_hip, left_knee, left_ankle)
                right_angle = calculate_angle(right_hip, right_knee, right_ankle)

                # 스쿼트 판정: 두 무릎 모두 앉은 상태 -> 일어난 상태
                if left_angle < 90 and right_angle < 90:  # 앉은 상태
                    if not is_squatting:
                        is_squatting = True
                elif left_angle > 160 and right_angle > 160:  # 일어난 상태
                    if is_squatting:
                        is_squatting = False
                        squat_count += 1

                # 성공 메시지
                if squat_count == number:
                    squat_completed = True
                    break

            except IndexError:
                pass
        if hand_detected ==True:
            cv2.putText(image, "Measuring!", (20, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        # 스쿼트 개수 표시 (항상 표시)
        cv2.putText(image, f"Count: {squat_count} / {number}", (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        # 랜드마크 시각화
        if pose_results.pose_landmarks:
            mp_drawing.draw_landmarks(image, pose_results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
        if hand_results.multi_hand_landmarks:
            for hand_landmarks in hand_results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

        cv2.imshow("Squat Counter", image)

        if cv2.waitKey(1) & 0xFF == ord('q'):  # 'q'를 눌러 종료
            squat_completed = False
            break

    camera.release()
    cv2.destroyAllWindows()
    return squat_completed

def push_up(number):
    mp_pose = mp.solutions.pose
    mp_hands = mp.solutions.hands       #정확도             #반응성
    pose = mp_pose.Pose(min_detection_confidence=0.8, min_tracking_confidence=0.8)
    hand = mp_hands.Hands(max_num_hands=1,min_detection_confidence=0.5, min_tracking_confidence=0.5)
    mp_drawing = mp.solutions.drawing_utils             #랜드마크를 동영상에 표시해주는 코드

    push_up_count = 0
    is_push_up = False
    is_push_up_detecting = False
    hand_detected=False

    # 비디오 스트림 열기
    camera = cv2.VideoCapture(0)

    while camera.isOpened():
        ret, frame = camera.read()
        if not ret:
            break

        # BGR 이미지를 RGB로 변환
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False

        # MediaPipe로 포즈와 손 분석
        pose_results = pose.process(image)      #mediapipe에서 사람의 포즈를 분석하기 위해서 사용
        hand_results = hand.process(image)      #mediapipe에서 사람의 손을 분석하기 위해서 사용

        # RGB 이미지를 다시 BGR로 변환
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        # 손 모양 확인 (보자기 모양 감지)
        if hand_detected==False:
            hand_detected=hand_detecting(hand_results,image)
        if hand_detected:
            is_push_up_detecting =True


        # 스쿼트 감지
        if is_push_up_detecting and pose_results.pose_landmarks:
            landmarks = pose_results.pose_landmarks.landmark        #관절의 좌표를 보여줌
            try:
                # 왼쪽 다리 좌표 (엉덩이, 무릎, 발목)
                left_hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x * frame.shape[1],
                            landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y * frame.shape[0]]
                left_knee = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x * frame.shape[1],
                             landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y * frame.shape[0]]
                left_ankle = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x * frame.shape[1],
                              landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y * frame.shape[0]]

                # 오른쪽 다리 좌표 (엉덩이, 무릎, 발목)
                right_hip = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x * frame.shape[1],
                             landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y * frame.shape[0]]
                right_knee = [landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x * frame.shape[1],
                              landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y * frame.shape[0]]
                right_ankle = [landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].x * frame.shape[1],
                               landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].y * frame.shape[0]]

                # 각도 계산
                left_angle = calculate_angle(left_hip, left_knee, left_ankle)
                right_angle = calculate_angle(right_hip, right_knee, right_ankle)

                # 스쿼트 판정: 두 무릎 모두 앉은 상태 -> 일어난 상태
                if left_angle < 90 and right_angle < 90:  # 앉은 상태
                    if not is_push_up:
                        is_push_up = True
                elif left_angle > 160 and right_angle > 160:  # 일어난 상태
                    if is_push_up:
                        is_push_up = False
                        push_up_count += 1

                # 성공 메시지
                if push_up_count == number:
                    push_up_completed = True
                    break

            except IndexError:
                pass
        if hand_detected ==True:
            cv2.putText(image, "Measuring!", (20, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        # 스쿼트 개수 표시 (항상 표시)
        cv2.putText(image, f"Count: {push_up_count} / {number}", (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        # 랜드마크 시각화
        if pose_results.pose_landmarks:
            mp_drawing.draw_landmarks(image, pose_results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
        if hand_results.multi_hand_landmarks:
            for hand_landmarks in hand_results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

        cv2.imshow("push_up Counter", image)

        if cv2.waitKey(1) & 0xFF == ord('q'):  # 'q'를 눌러 종료
            return False

    camera.release()
    cv2.destroyAllWindows()
    return push_up_completed

def calculate_angle(point1, point2, point3):
    """
    주어진 세 점의 좌표로 각도를 계산하는 함수.
    벡터의 크기를 사용해 코싸인 함수로 각도를 구함.
    """
    a = np.array(point1)  # Hip
    b = np.array(point2)  # Knee
    c = np.array(point3)  # Ankle
    
    ab = a - b
    bc = c - b
    
    cosine_angle = np.dot(ab, bc) / (np.linalg.norm(ab) * np.linalg.norm(bc))
    angle = np.arccos(cosine_angle)
    return np.degrees(angle)

def hand_detecting(hand_results,image):
    if  hand_results.multi_hand_landmarks:      #손의 랜드마크 리스트(관절 21개를 의미)
            hand_landmarks=hand_results.multi_hand_landmarks[0] #인식한 손 가져오기
            
            finger_1=False      #엄지손가락
            finger_2=False      #검지손가락
            finger_3=False      #중지손가락
            finger_4=False      #약지손가락
            finger_5=False      #새끼손가락

            if(hand_landmarks.landmark[4].y<hand_landmarks.landmark[2].y):
                finger_1=True
            if(hand_landmarks.landmark[8].y<hand_landmarks.landmark[6].y):
                finger_2=True
            if(hand_landmarks.landmark[12].y<hand_landmarks.landmark[10].y):
                finger_3=True
            if(hand_landmarks.landmark[16].y<hand_landmarks.landmark[14].y):
                finger_4=True
            if(hand_landmarks.landmark[20].y<hand_landmarks.landmark[18].y):
                finger_5=True

            if(finger_1 and finger_2 and finger_3 and finger_4 and finger_5):
                cv2.putText(image, "Start Detection!", (20, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                return True
    return False

print(A=exercise("LUNGE",30))

