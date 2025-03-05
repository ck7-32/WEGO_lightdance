import cv2
import mediapipe as mp
import json
import numpy as np

# 初始化 Mediapipe Pose
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(static_image_mode=False, min_detection_confidence=0.5, min_tracking_confidence=0.5)

# 打開影片
cap = cv2.VideoCapture("chinodance2.MOV")
pose_data = []  # 儲存每幀的骨架數據
simplified_pose_data = {"data": [],"depth":[]}  # 簡化數據
cY=None
scale_factor=None
frame_index = 0  # 幀數計數

setdetectpoint =[0,13,14,15,16,25,26]
setdetectpointM=[23,24]
detectpoint=[]
detectpointM=0
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

        # 取得左、右髖部和肩膀的標記點，轉換為像素座標
        left_hip = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_HIP]
        right_hip = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_HIP]
        left_shoulder = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER]
        right_shoulder = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_SHOULDER]
        if cY==None:
            cY = (left_hip.y + right_hip.y + left_shoulder.y + right_shoulder.y) / 4 * height
            print(cY)

        # 計算中心點（像素座標）
        center_x = (left_hip.x + right_hip.x + left_shoulder.x + right_shoulder.x) / 4 * width
        frame_data["center"] = {"x": center_x, "y": cY}

        # 計算人物的實際高度（像素）
        if scale_factor==None:
            hip_to_shoulder_distance = ((left_hip.x * width - left_shoulder.x * width) ** 2 +
                                        (left_hip.y * height - left_shoulder.y * height) ** 2) ** 0.5
            scale_factor = 50 / hip_to_shoulder_distance  # 計算縮放比例

        simplified_frame = []  # 儲存簡化後的幀數據
        detectpoint =[] # 儲存簡化後的幀數據
        detectpointM=0
        # 處理每個關鍵點
        for i, lm in enumerate(results.pose_landmarks.landmark):
            pixel_x = lm.x * width
            pixel_y = lm.y * height

            # 轉換為相對於中心點的縮放座標
            relative_x = (pixel_x - center_x) * scale_factor
            relative_y = (pixel_y - cY) * scale_factor
            relative_z = lm.z * scale_factor

            frame_data["relative_landmarks"].append({
                "x": relative_x,
                "y": relative_y,
                "z": relative_z,
                "visibility": lm.visibility
            })

            # 只保留指定的關鍵點
      

            if i==0 or i==2 or i==5 or 11 <= i <= 28:
                simplified_frame.append([relative_x, relative_y, relative_z])
            if i in setdetectpoint:
                detectpoint.append(relative_z)
            if i in setdetectpointM:
                detectpointM+=relative_z
        detectpoint.append(detectpointM/2)
        pose_data.append(frame_data)
        simplified_pose_data["data"].append(simplified_frame)
        sorted_indices = np.argsort(detectpoint).tolist()
        simplified_pose_data["depth"].append(sorted_indices)
    frame_index += 1

# 釋放影片資源
cap.release()

# 儲存完整骨架數據至 JSON 檔案
with open("relative_pose_data_pixels.json", "w") as f:
    json.dump(pose_data, f, indent=4)

# 儲存簡化骨架數據至 JSON 檔案，格式化換行
with open("data\dance.json", "w") as f:
    f.write('{\n    "data": [\n')
    for i, frame in enumerate(simplified_pose_data["data"]):
        frame_str = "        " + json.dumps(frame, separators=(',', ':'))
        if i < len(simplified_pose_data["data"])-1 :
            frame_str += ","
        f.write(frame_str + "\n")
    f.write('\n    ],"depth": [\n')
    # 處理二維陣列的 `depth`
    depth = simplified_pose_data["depth"]
    
        
    for i, row in enumerate(depth):
        row_str = "        " +json.dumps(row, separators=(',', ':'))
        if i < len(depth) - 1:
            row_str += ","
        f.write(row_str + "\n")
    f.write('\n    ]\n}\n')
print("骨架數據已儲存至 relative_pose_data_pixels.json 和 simplified_pose_data.json")
