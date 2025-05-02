import RPi.GPIO as GPIO
import time

# 핀 번호 설정
BUTTON_PIN = 18  # 버튼이 연결될 GPIO 핀 번호
BLUE_PIN = 17
GREEN_PIN = 22
RED_PIN = 27

# 글로벌 변수
led_state = 0  # LED 상태 (0: 모두 꺼짐, 1: 파란색, 2: 초록색, 3: 빨간색)

# GPIO 설정 함수
def setup_gpio():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(BLUE_PIN, GPIO.OUT)
    GPIO.setup(GREEN_PIN, GPIO.OUT)
    GPIO.setup(RED_PIN, GPIO.OUT)

# 모든 LED 끄는 함수
def turn_off_leds():
    global led_state
    led_state = 0
    GPIO.output(BLUE_PIN, GPIO.LOW)
    GPIO.output(GREEN_PIN, GPIO.LOW)
    GPIO.output(RED_PIN, GPIO.LOW)

# LED 상태 변경 함수
def change_led_state():
    global led_state
    led_state += 1
    if led_state > 3:
        led_state = 1
    if led_state == 1:
        GPIO.output(BLUE_PIN, GPIO.HIGH)
        GPIO.output(GREEN_PIN, GPIO.LOW)
        GPIO.output(RED_PIN, GPIO.LOW)
    elif led_state == 2:
        GPIO.output(BLUE_PIN, GPIO.LOW)
        GPIO.output(GREEN_PIN, GPIO.HIGH)
        GPIO.output(RED_PIN, GPIO.LOW)
    elif led_state == 3:
        GPIO.output(BLUE_PIN, GPIO.LOW)
        GPIO.output(GREEN_PIN, GPIO.LOW)
        GPIO.output(RED_PIN, GPIO.HIGH)

# 버튼 이벤트 콜백 함수
def button_callback(channel):
    start_time = time.time()

    while GPIO.input(channel) == GPIO.LOW:  #눌렸을 땐 LOW
        time.sleep(0.01) 

    button_press_duration = time.time() - start_time
    if button_press_duration >= 1:  # 1초 이상 누르면 LED 끄기
        turn_off_leds()
    else:  # 짧게 누르면 LED 색상 변경
        change_led_state()

# GPIO 종료 함수
def cleanup_gpio():
    GPIO.cleanup()

# 메인 함수
def main():
    setup_gpio()

    turn_off_leds()
    # 버튼 이벤트 감지 설정
    # GPIO.FALLING은 누르는 순간(LOW) 이벤트 발생
    GPIO.add_event_detect(BUTTON_PIN, GPIO.FALLING, callback=button_callback, bouncetime=300)

    try:
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt:
        pass
    finally:
        cleanup_gpio()

if __name__ == "__main__":
    main()



