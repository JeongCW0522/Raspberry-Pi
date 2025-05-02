import RPi.GPIO as GPIO
import time
# GPIO 모드 설정
GPIO.setmode(GPIO.BCM)
# LED 핀 설정
LED_PIN = 18
GPIO.setup(LED_PIN, GPIO.OUT)
# PWM 인스턴스 생성
pwm = None
pwm = GPIO.PWM(LED_PIN, 10000)
pwm.start(0)  # 초기 듀티 사이클 0
try:
    while True:
        # 점점 밝아짐
        for dc in range(0, 101, 2):
            pwm.ChangeDutyCycle(dc)
            print("밝아 짐", dc)
            time.sleep(0.1)
        time.sleep(2)
        # 점점 어두워짐
        for dc in range(100, -1, -2):
            print("어두워 짐", dc)
            pwm.ChangeDutyCycle(dc)
            time.sleep(0.1)
        time.sleep(1)
except KeyboardInterrupt:
    # Ctrl+C 눌렀을 때 실행 종료
    pass  
finally:
    if pwm is not None:
        try:
            pwm.stop()
        except:
            pass
        del pwm  # __del__ 호출 시 오류 방지
    GPIO.cleanup()