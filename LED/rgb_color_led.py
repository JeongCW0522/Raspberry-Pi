import RPi.GPIO as GPIO
import time

# 핀 번호 설정
BUTTON_PIN =18
BLUE_PIN =17
GREEN_PIN =22
RED_PIN =27

# LED 색의 정보는 배열에 담음
led_states = [
  (GPIO.LOW, GPIO.LOW, GPIO.HIGH),  #빨강
  (GPIO.LOW, GPIO.HIGH, GPIO.LOW),  #초록
  (GPIO.HIGH, GPIO.LOW, GPIO.LOW),  #파랑
  (GPIO.LOW, GPIO.HIGH, GPIO.HIGH),  #노랑
  (GPIO.HIGH, GPIO.LOW, GPIO.HIGH),  #하늘
  (GPIO.HIGH, GPIO.HIGH, GPIO.LOW),  #보라
  (GPIO.HIGH, GPIO.HIGH, GPIO.HIGH),  #흰색
  (GPIO.LOW, GPIO.LOW, GPIO.LOW)   #LOW
]

led_index =0 # 현재 LED 상태의 인덱스 값

# GPIO 설정 함수
def setup_gpio():
  GPIO.setmode(GPIO.BCM)
  GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
  GPIO.setup(BLUE_PIN, GPIO.OUT)
  GPIO.setup(GREEN_PIN, GPIO.OUT)
  GPIO.setup(RED_PIN, GPIO.OUT)

# LED를 모두 끄는 함수
def turn_off_leds():
  global led_index
  led_index = len(led_states) -1  # OFF 상태의 인덱스로 변경
  GPIO.output(BLUE_PIN, GPIO.LOW)
  GPIO.output(GREEN_PIN, GPIO.LOW)
  GPIO.output(RED_PIN, GPIO.LOW)

# LED의 색상을 변경하는 함수
def change_led_state():
  global led_index
  led_index = (led_index +1) %len(led_states)  # 다음 LED 상태로 이동
  GPIO.output(BLUE_PIN, led_states[led_index][0])
  GPIO.output(GREEN_PIN, led_states[led_index][1])
  GPIO.output(RED_PIN, led_states[led_index][2])

# 버튼 이벤트 콜백 함수
def button_callback(channel):
  start_time =time.time()

  while GPIO.input(BUTTON_PIN) == GPIO.LOW:
    time.sleep(0.01) 

  button_press_duration =time.time() -start_time
  if button_press_duration >=1: 
    turn_off_leds()
  else: 
    change_led_state()

# GPIO 종료 함수
def cleanup_gpio():
  GPIO.cleanup()

# 메인 함수
def main():
  setup_gpio()
  turn_off_leds()
  GPIO.add_event_detect(BUTTON_PIN, GPIO.FALLING, callback=button_callback, bouncetime=300)

  try:
    while True:
      time.sleep(0.1)
  except KeyboardInterrupt:
    pass
  finally:
    cleanup_gpio()

if __name__=="__main__":
  main()
