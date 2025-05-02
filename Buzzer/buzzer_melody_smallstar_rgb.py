import RPi.GPIO as GPIO
import time

# 핀 번호 설정
BLUE_PIN =24
GREEN_PIN =23
RED_PIN =18
BUZZER_PIN =17

# GPIO 설정 함수
def setup_gpio():
  GPIO.setmode(GPIO.BCM)
  GPIO.setup(BLUE_PIN, GPIO.OUT, initial = GPIO.LOW)
  GPIO.setup(GREEN_PIN, GPIO.OUT, initial = GPIO.LOW)
  GPIO.setup(RED_PIN, GPIO.OUT, initial = GPIO.LOW)
  GPIO.setup(BUZZER_PIN, GPIO.OUT)

setup_gpio()

pwm =None
# PWM 인스턴스 생성 및 초기 주파수(100Hz) 설정
pwm = GPIO.PWM(BUZZER_PIN, 100) 
pwm.start(0) 

# 주요 음표의 주파수 (단위: Hz)
notes = {
  'C4': 261.63, #도
  'D4': 293.66, #레
  'E4': 329.63, #미
  'F4': 349.23, #파
  'G4': 392.00, #솔
  'A4': 440.00, #라
  'B4': 493.88, #시
  'C5': 523.25 # 추가된 높은 도 음표
}

# 각 음표에 대한 RGB 값 설정
colors = {
    'C4': (1, 0, 0),  # 빨강
    'D4': (0, 1, 0),  # 초록
    'E4': (0, 0, 1),  # 파랑
    'F4': (1, 1, 0),  # 노랑
    'G4': (0, 1, 1),  # 하늘
    'A4': (1, 0, 1),  # 보라
    'B4': (1, 1, 1),  # 흰색
    'C5': (1, 0, 0)   # 빨강
}

def set_color(r, g, b):
  GPIO.output(RED_PIN, r)
  GPIO.output(GREEN_PIN, g)
  GPIO.output(BLUE_PIN, b)

# 간단한 멜로디 (음표와 지속 시간)
melody = [('C4', 0.5), ('C4', 0.5), ('G4', 0.5), ('G4', 0.5), ('A4', 0.5), ('A4', 0.5), ('G4', 1),
('F4', 0.5), ('F4', 0.5), ('E4', 0.5), ('E4', 0.5), ('D4', 0.5), ('D4', 0.5), ('C4', 1),
('G4', 0.5), ('G4', 0.5), ('F4', 0.5), ('F4', 0.5), ('E4', 0.5), ('E4', 0.5), ('D4', 1),
('G4', 0.5), ('G4', 0.5), ('F4', 0.5), ('F4', 0.5), ('E4', 0.5), ('E4', 0.5), ('D4', 1),
('C4', 0.5), ('C4', 0.5), ('G4', 0.5), ('G4', 0.5), ('A4', 0.5), ('A4', 0.5), ('G4', 1),
('F4', 0.5), ('F4', 0.5), ('E4', 0.5), ('E4', 0.5), ('D4', 0.5), ('D4', 0.5), ('C4', 1)
] 

def play(note, duration):
  pwm.ChangeFrequency(notes[note])
  pwm.ChangeDutyCycle(50) # 켜짐
  set_color(*colors[note]) # LED 색상 변경

  time.sleep(duration) # 음표 지속 시간
  pwm.ChangeDutyCycle(0) # 꺼짐
  set_color(0, 0, 0) # LED 끄기
  
try: 
  for note, duration in melody:
    play(note, duration)
    time.sleep(0.1) # 음표 사이의 간격
except KeyboardInterrupt:  
        # Ctrl+C 눌렀을 때 실행 종료
  pass
finally:
  if pwm is not None:
    try:
      pwm.stop()
    except:
      pass
    del pwm 
  GPIO.cleanup()
