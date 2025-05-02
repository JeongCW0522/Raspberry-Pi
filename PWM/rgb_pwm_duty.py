import RPi.GPIO as GPIO
import time

#핀 설정
GPIO.setmode(GPIO.BCM)
R_PIN = 18 
G_PIN = 23
GPIO.setup(R_PIN, GPIO.OUT)
GPIO.setup(G_PIN, GPIO.OUT)
pwm_r = None
pwm_g = None
pwm_r = GPIO.PWM(R_PIN, 10000)
pwm_g = GPIO.PWM(G_PIN, 10000)
pwm_r.start(0)
pwm_g.start(0)

try:
    while True:
        for g in range(50, 101, 5):      # 주황 → 노랑
            pwm_r.ChangeDutyCycle(100)
            pwm_g.ChangeDutyCycle(g)
            time.sleep(0.1)
        print("주황 -> 노랑")
        time.sleep(1.5)
        for r in range(100, 49, -5):     # 노랑 → 연두
            pwm_r.ChangeDutyCycle(r)
            pwm_g.ChangeDutyCycle(100)
            time.sleep(0.1)
        print("노랑 -> 연두")
        time.sleep(1.5)            
        for g in range(100, 29, -5):     # 연두 → 갈색
            pwm_r.ChangeDutyCycle(50)
            pwm_g.ChangeDutyCycle(g)
            time.sleep(0.1)
        print("연두 -> 갈색")
        time.sleep(1.5)  
        for r in range(50, 101, 5):      # 갈색 → 주황
            pwm_r.ChangeDutyCycle(r)
            pwm_g.ChangeDutyCycle(30)
            time.sleep(0.1)
        print("갈색 -> 주황")
        time.sleep(1.5)
except KeyboardInterrupt:
    # Ctrl+C 눌렀을 때 실행 종료
    pass        
finally:
    if pwm_r is not None:
        try:
            pwm_r.stop()
        except:
            pass
        del pwm_r 

    if pwm_g is not None:
        try:
            pwm_g.stop()
        except:
            pass
        del pwm_g 
    GPIO.cleanup()