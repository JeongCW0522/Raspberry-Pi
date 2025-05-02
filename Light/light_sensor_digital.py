import RPi.GPIO as GPIO
import time
# GPIO 핀 번호 설정
SENSOR_PIN = 17  
# GPIO 설정
GPIO.setmode(GPIO.BCM)  
GPIO.setup(SENSOR_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # 내부 풀다운 저항 사용
print('조도 센서 값 읽기 시작...')
try:
    while True:
        sensor_value = GPIO.input(SENSOR_PIN)
        if sensor_value == GPIO.HIGH:
            print('조도가 낮습니다.')   #어두워 질 때 감지
        else:
            print('조도가 높습니다.')
        time.sleep(1)
except KeyboardInterrupt:
    print("프로그램 종료")
finally:
    GPIO.cleanup()