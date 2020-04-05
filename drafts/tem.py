import Adafruit_DHT as dht
import time
#获取环境温度温度
def get_temp_hum():
  sensor = dht.DHT22
  pin = 4
  humidity, temperature = dht.read_retry(sensor, pin)
  if humidity is not None and temperature is not None:
    return round(temperature,2), round(humidity,2)#返回结果,精确2位
  else:
    return 0, 0
while True:
  print(get_temp_hum()) #输出结果
  time.sleep(10)
