
#!/usr/bin//env python
# -*- coding:utf-8 -*-
import smbus   
import time
 
address = 0x48 ## address  ---> 器件的地址(硬件地址 由器件决定)
A0 = 0x40      ##  A0    ----> 器件某个端口的地址（数据存储的寄存器）
A1 = 0x41
A2 = 0x42
A3 = 0x43
bus = smbus.SMBus(1) ## 开启总线
while True: ##循环查询
    bus.write_byte(address,A0)  ## 告诉树莓派 你想获取那个器件的那个端口的数据
    value = 143-bus.read_byte(address) ## 获得数据
    print("当前温度:%1.0f  ℃ " %(value)) ##打印数据
    time.sleep(1) ##延迟1秒
