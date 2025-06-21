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
# --- GPIO 설정 ---
LED_PIN = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT)
# --- Flask-SocketIO 설정 ---
app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode="eventlet")
# --- DHT22 센서 설정 ---
dht_device = adafruit_dht.DHT22(board.D18)
# --- LED 상태 반환 함수 ---
def get_led_state():
    return "on" if GPIO.input(LED_PIN) else "off"
# --- LED 제어 처리 ---
@socketio.on("led_control")
def control_led(data):
    state = data.get("state")
    if state == "on":
        GPIO.output(LED_PIN, GPIO.HIGH)
    elif state == "off":
        GPIO.output(LED_PIN, GPIO.LOW)
    state = get_led_state()
    print(f"led 상태 : {state}")
    socketio.emit("led_status", {"state": state})

# --- LED 상태 요청 처리 ---
@socketio.on("get_led_status")
def handle_status_request():
    state = get_led_state()
    print(f"led 상태 : {state}")
    socketio.emit("led_status", {"state": state}, room=request.sid)

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
    t = threading.Thread(target=temperature_monitor_thread)  # 실행 함수 작성
    t.daemon = True  # 메인 쓰레드 종료 시 같이 종료
    t.start()

# --- 메인 ---
if __name__ == "__main__":
    print("서버 시작")
    start_sensor_thread()
    socketio.run(app, host="0.0.0.0", port=5000)