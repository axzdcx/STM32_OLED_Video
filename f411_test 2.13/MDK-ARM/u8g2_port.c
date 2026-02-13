#include "u8g2.h"
#include "main.h"  // 确保包含了 HAL 库和你的 I2C 定义
#include "i2c.h"   // CubeMX 生成的 I2C 头文件

// 1. 硬件 I2C 传输回调函数
uint8_t u8x8_byte_stm32_hw_i2c(u8x8_t *u8x8, uint8_t msg, uint8_t arg_int, void *arg_ptr)
{
    static uint8_t buffer[32]; 
    static uint8_t buf_idx;
    uint8_t *data;

    switch(msg)
    {
        case U8X8_MSG_BYTE_SEND:
            data = (uint8_t *)arg_ptr;
            while( arg_int > 0 )
            {
                buffer[buf_idx++] = *data;
                data++;
                arg_int--;
            }
            break;
        case U8X8_MSG_BYTE_INIT:
            // I2C 已经在 main 里的 MX_I2C1_Init 初始化过了，这里不用动
            break;
        case U8X8_MSG_BYTE_SET_DC:
            // I2C 不需要 DC 引脚，留空
            break;
        case U8X8_MSG_BYTE_START_TRANSFER:
            buf_idx = 0;
            break;
        case U8X8_MSG_BYTE_END_TRANSFER:
            // 发送数据：地址是 0x78 (或者是 0x3C << 1)
            HAL_I2C_Master_Transmit(&hi2c1, 0x78, buffer, buf_idx, 1000);
            break;
        default:
            return 0;
    }
    return 1;
}

// 2. 延时回调函数
uint8_t u8x8_gpio_and_delay_stm32(u8x8_t *u8x8, uint8_t msg, uint8_t arg_int, void *arg_ptr)
{
    switch(msg)
    {
        case U8X8_MSG_GPIO_AND_DELAY_INIT:
            break;
        case U8X8_MSG_DELAY_MILLI:
            HAL_Delay(arg_int);
            break;
        case U8X8_MSG_DELAY_10MICRO:
            // 简单的微秒延时，大概即可
            for (uint32_t n = 0; n < arg_int * 72; n++) {__NOP();}
            break;
        case U8X8_MSG_DELAY_100NANO:
            __NOP();
            break;
    }
    return 1;
}
