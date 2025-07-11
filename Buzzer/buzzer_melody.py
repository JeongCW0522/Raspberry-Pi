import RPi.GPIO as GPIO
import time
# GPIO 모드 설정
GPIO.setmode(GPIO.BCM)

BUZZER_PIN =17 # 17번 핀에 부저 사용한다
GPIO.setup(BUZZER_PIN, GPIO.OUT)
pwm = None
# PWM 인스턴스 생성 및 초기 주파수 설정
pwm =GPIO.PWM(BUZZER_PIN, 100) # 초기 주파수 100Hz 설정
pwm.start(0) 

# 주요 음표의 주파수 (단위: Hz)
notes = {
  'C4': 261.63,
  'D4': 293.66,
  'E4': 329.63,
  'F4': 349.23,
  'G4': 392.00,
  'A4': 440.00,
  'B4': 493.88,
  'C5': 523.25 # 추가된 높은 도 음표
}
# 간단한 멜로디 (음표, 지속 시간)
melody = [('C4', 0.5), ('D4', 0.5), ('E4', 0.5), ('F4', 1.5),
     ('G4', 0.5), ('A4', 0.5), ('B4', 0.5), ('C5', 0.5)]

def play(note, duration):
   print(f"Playing note: {note}")
  pwm.ChangeFrequency(notes[note]) # 음표별 주파수로 변경
  pwm.ChangeDutyCycle(20) # 켜짐
  time.sleep(duration) # 음표 지속 시간
  pwm.ChangeDutyCycle(0) # 꺼짐
try: 
  for note, duration in melody:
    play(note, duration)
    time.sleep(0.1) # 음표 사이의 간격
finally:
  if pwm is not None:
    try:
      pwm.stop()
    except:
      pass
    del pwm # pwm 삭제해 재사용 방지
  GPIO.cleanup()