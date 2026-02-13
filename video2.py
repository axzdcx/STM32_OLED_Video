import cv2
import serial
import numpy as np
import time
import os

# ================= 配置区 =================
COM_PORT = 'COM15'       # 请修改为你的端口号
BAUD_RATE = 921600       # 请修改为你 STM32 设定的波特率
VIDEO_FILE = 'video.mp4' # 视频文件名 (必须放在同级目录下)
# =========================================

# 0. 检查视频文件是否存在
if not os.path.exists(VIDEO_FILE):
    print(f"错误：找不到文件 '{VIDEO_FILE}'")
    exit()

# 1. 连接串口
try:
    ser = serial.Serial(COM_PORT, BAUD_RATE, timeout=0.1)
    print(f"成功连接 {COM_PORT}")
except Exception as e:
    print(f"串口连接失败: {e}")
    exit()

# 2. 打开视频
cap = cv2.VideoCapture(VIDEO_FILE)
print("按 'q' 键退出")

while True:
    ret, frame = cap.read()
    
    # --- 循环播放逻辑 ---
    
    if not ret:
        print("播放结束，重新开始...")
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0) # 倒带回第 0 帧
        continue

    # --- 图像处理 ---
    # 1. 强制缩放成 128x64
    img_resized = cv2.resize(frame, (128, 64))
    
    # 2. 转灰度
    img_gray = cv2.cvtColor(img_resized, cv2.COLOR_BGR2GRAY)
    
    # 3. 二值化
    
    _, img_binary = cv2.threshold(img_gray, 128, 255, cv2.THRESH_BINARY)

    # --- 预览窗口 ---
    
    preview_img = cv2.resize(img_binary, (640, 320), interpolation=cv2.INTER_NEAREST)
    cv2.imshow("Video2 Player (Bad Apple)", preview_img)

    # --- 数据打包与发送 ---
    # 1. 转成 0/1 矩阵
    img_data = (img_binary > 128).astype(np.uint8)
    # 2. 压缩成 XBM 字节流 (低位在前)
    packed_data = np.packbits(img_data, axis=1, bitorder='little')

    # 3. 发送数据 (关键：加帧头 0xFE)
    try:
        ser.write(b'\xFE' + packed_data.tobytes())
    except:
        break

    # --- 速度控制 ---
    # 视频通常是 30帧 (0.033秒)，如果你觉得卡，可以把这个数改小
    # 如果花屏，就把这个数改大 (比如 0.03)
    time.sleep(0.04) 

    # --- 按键退出 ---
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
ser.close()