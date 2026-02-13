## STM32 OLED 播放视频及摄像头实时图传

示例型号为 **STM32F411** ，通过 Python 上位机处理视频数据并利用串口协议推送到嵌入式端，在 0.96 寸 OLED 屏幕上实现画面显示。

---


### 硬件连接
| 模块 | 引脚 (STM32) | 说明 |
| :--- | :--- | :--- |
| **OLED (I2C1)** | SCL -> PB6 / SDA -> PB7 | 高速 I2C 模式 (400kHz) |
| **DAPLink/TTL** | TX -> PA10 (RX1) | 串口通讯引脚 |
| **GND** | GND | 共地以保证信号稳定 |

### 快速使用
1.  **硬件端**：在 `main.c` 中配置好 U8g2 驱动并开启串口中断，将编译后的固件烧录至单片机。
2.  **环境配置**：
    ```bash
    pip install opencv-python pyserial numpy
    ```
3.  **运行程序**：
     运行摄像头直播：`python video.py`
     运行视频播放：`python video2.py`
