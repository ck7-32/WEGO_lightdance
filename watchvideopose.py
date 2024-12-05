import cv2
import mediapipe as mp
import json

# 初始化 Mediapipe Pose 和繪圖工具
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils
pose = mp_pose.Pose(static_image_mode=False, min_detection_confidence=0.5, min_tracking_confidence=0.5)

# 打開影片
cap = cv2.VideoCapture("chinodance2.MOV")
pose_data = []  # 儲存每幀的骨架數據

frame_index = 0  # 幀數計數
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # 取得影像的寬度和高度
    height, width, _ = frame.shape

    # 將影像轉為 RGB 格式，適合 Mediapipe 的處理
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # 使用 Mediapipe 偵測姿勢
    results = pose.process(frame_rgb)

    # 如果偵測到骨架數據
    if results.pose_landmarks:
        frame_data = {
            "frame": frame_index,
            "center": None,
            "relative_landmarks": []
        }

        # 繪製骨架數據到影像上
        mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

        # 取得左、右髖部和肩膀的標記點，轉換為像素座標
        left_hip = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_HIP]
        right_hip = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_HIP]
        left_shoulder = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER]
        right_shoulder = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_SHOULDER]

        # 計算中心點（像素座標）
        center_x = (left_hip.x + right_hip.x + left_shoulder.x + right_shoulder.x) / 4 * width
        center_y = (left_hip.y + right_hip.y + left_shoulder.y + right_shoulder.y) / 4 * height
        frame_data["center"] = {"x": center_x, "y": center_y}

        # 計算人物的實際高度（像素）
        hip_to_shoulder_distance = ((left_hip.x * width - left_shoulder.x * width) ** 2 +
                                    (left_hip.y * height - left_shoulder.y * height) ** 2) ** 0.5
        scale_factor = 80 / hip_to_shoulder_distance  # 計算縮放比例

        # 處理每個關鍵點
        for lm in results.pose_landmarks.landmark:
            pixel_x = lm.x * width
            pixel_y = lm.y * height

            # 轉換為相對於中心點的縮放座標
            relative_x = (pixel_x - center_x) * scale_factor
            relative_y = (pixel_y - center_y) * scale_factor

            frame_data["relative_landmarks"].append({
                "x": relative_x,
                "y": relative_y,
                "z": lm.z * scale_factor,
                "visibility": lm.visibility
            })

        pose_data.append(frame_data)

    # 顯示處理後的影像
    cv2.imshow("Pose Detection", frame)

    # 按下 'q' 鍵可退出
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    frame_index += 1

# 釋放影片資源
cap.release()
cv2.destroyAllWindows()

# 儲存骨架數據至 JSON 檔案
with open("relative_pose_data_pixels.json", "w") as f:
    json.dump(pose_data, f, indent=4)

print("骨架數據已儲存至 relative_pose_data_pixels.json")
