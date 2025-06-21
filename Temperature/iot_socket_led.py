import time
import threading
from flask import Flask, request
from flask_socketio import SocketIO
import RPi.GPIO as GPIO
import board
import adafruit_dht

# --- 글로벌 변수 ---
latest_temp = None
latest_hum = None
led_enabled = False  # 사용자가 웹에서 LED를 ON 했는 지 상태 저장

# --- GPIO 설정 ---
BLUE_PIN = 17  # 파랑(B)
RED_PIN = 24   # 빨강(R)

GPIO.setmode(GPIO.BCM)
GPIO.setup(BLUE_PIN, GPIO.OUT)
GPIO.setup(RED_PIN, GPIO.OUT)

# --- Flask-SocketIO 설정 ---
app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode="eventlet")

# --- DHT22 센서 설정 ---
dht_device = adafruit_dht.DHT22(board.D18)

# --- LED 상태 반환 함수 ---
def get_led_state():
    return "on" if led_enabled else "off"

# --- RGB LED 색상 제어 함수 ---
def set_rgb_color(red_on, blue_on):
    GPIO.output(RED_PIN, GPIO.HIGH if red_on else GPIO.LOW)
    GPIO.output(BLUE_PIN, GPIO.HIGH if blue_on else GPIO.LOW)

# --- LED 제어 처리 (사용자 요청에 따라 on/off) ---
@socketio.on("led_control")
def control_led(data):
    global led_enabled
    state = data.get("state")
    if state == "on":
        led_enabled = True
    elif state == "off":
        led_enabled = False
        set_rgb_color(False, False)  # 끌 때는 RGB 모두 꺼짐
    print(f"led 상태 : {get_led_state()}")
    socketio.emit("led_status", {"state": get_led_state()})

# --- LED 상태 요청 처리 ---
@socketio.on("get_led_status")
def handle_status_request():
    print(f"led 상태 : {get_led_state()}")
    socketio.emit("led_status", {"state": get_led_state()}, room=request.sid)

# --- 온습도 상태 요청 처리 (유니캐스트) ---
@socketio.on("get_temperature_humidity_status")
def send_temperature_humidity_status():
    if latest_temp is not None and latest_hum is not None:
        socketio.emit("temperature_humidity_status", {
            "temp": latest_temp,
            "hum": latest_hum
        }, room=request.sid)
    else:
        socketio.emit("temperature_humidity_status", {
            "temp": "N/A",
            "hum": "N/A"
        }, room=request.sid)

# --- 센서 측정 스레드 ---
def temperature_monitor_thread():
    global latest_temp, latest_hum
    while True:
        try:
            temp = dht_device.temperature
            hum = dht_device.humidity
            if hum is not None and temp is not None:
                latest_temp = round(temp, 1)
                latest_hum = round(hum, 1)
                print(f"센서 측정: {latest_temp}℃ / {latest_hum}%")

                # --- 자동 LED 제어 조건 ---
                if led_enabled:
                    if latest_temp >= 24:
                        set_rgb_color(red_on=True, blue_on=False)
                    else:
                        set_rgb_color(red_on=False, blue_on=True)

            else:
                print("센서 데이터 없음")
        except RuntimeError as e:
            print("센서 에러:", e.args[0])
        except Exception as e:
            dht_device.exit()
            raise e
        time.sleep(2)

# --- 센서 스레드 시작 ---
def start_sensor_thread():
    t = threading.Thread(target=temperature_monitor_thread)
    t.daemon = True
    t.start()

# --- 메인 ---
if __name__ == "__main__":
    print("서버 시작")
    start_sensor_thread()
    socketio.run(app, host="0.0.0.0", port=5000)
