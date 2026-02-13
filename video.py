import cv2
import serial
import numpy as np
import time

# ================= 配置区 =================
# 1. 修改串口号 
COM_PORT = 'COM15'  
# 2. 波特率必须和 STM32 一样
BAUD_RATE = 115200 
# =========================================

# 连接串口
try:
    ser = serial.Serial(COM_PORT, BAUD_RATE, timeout=0.1)
    print(f"成功连接 {COM_PORT} @ {BAUD_RATE}")
except Exception as e:
    print(f"串口连接失败: {e}")
    exit()

# 打开摄像头 (0 是默认摄像头，也可以填 'xxx.mp4' 文件路径)
cap = cv2.VideoCapture(0)

print("按 'q' 退出，按 't' 切换二值化阈值模式")

threshold_val = 128 # 默认阈值

while True:
    ret, frame = cap.read()
    if not ret:
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0) # 视频播完循环播放
        continue

    # 1. 缩放：强制变形成 128x64
    img_resized = cv2.resize(frame, (128, 64))

    # 2. 转灰度
    img_gray = cv2.cvtColor(img_resized, cv2.COLOR_BGR2GRAY)

    # 3. 二值化处理 (把灰度图变成纯黑白)
    
    img_binary = cv2.adaptiveThreshold(img_gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    
    # 4. 预览窗口
    cv2.imshow("PC Preview", img_binary)

    # 5. 数据打包
   
    img_data = (img_binary > 128).astype(np.uint8)
    packed_data = np.packbits(img_data, axis=1, bitorder='little')
    
    # 6. 发送数据 (1024 字节)
    try:
       ser.write(b'\xFE' + packed_data.tobytes()) 
    except:
        break
    time.sleep(0.1)
    # 按键控制
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    elif key == ord('t'): # 按 t 键自动寻找最佳阈值(Otsu算法)
        threshold_val, _ = cv2.threshold(img_gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        print(f"自动阈值: {threshold_val}")

cap.release()
cv2.destroyAllWindows()
ser.close()