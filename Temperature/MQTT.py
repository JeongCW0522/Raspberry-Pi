import time
import threading
from flask import Flask, request
from flask_socketio import SocketIO
import RPi.GPIO as GPIO
import board
import adafruit_dht
import paho.mqtt.client as mqtt  

# --- MQTT 클라이언트 설정 ---
def on_connect(client, userdata, flags, rc):
    print("MQTT 연결됨:", rc)  # MQTT 브로커에 연결되면 호출되는 콜백 함수

mqtt_client = mqtt.Client(protocol=mqtt.MQTTv311)      # MQTT 클라이언트 객체 생성 (v3.1.1 프로토콜 명시)
mqtt_client.on_connect = on_connect                    # 연결 콜백 등록 → 경고 방지 및 상태 확인용
mqtt_client.reconnect_delay_set(min_delay=1, max_delay=30)  # 재연결 지연 시간 설정 (최소 1초, 최대 30초)
mqtt_client.connect_async("localhost", 1883, 60)       # 비동기 방식으로 Mosquitto 브로커에 연결 시도
mqtt_client.loop_start()                               # 내부 네트워크 루프 실행 (백그라운드 스레드에서 처리)

# --- 글로벌 변수 ---
latest_temp = None  # 최근 측정된 온도 저장 변수
latest_hum = None  # 최근 측정된 습도 저장 변수

# --- GPIO 설정 ---
LED_PIN = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT)

# --- Flask-SocketIO 설정 ---
app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode="eventlet")  # 비동기 통신을 위한 SocketIO 설정

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
    socketio.emit("led_status", {"state": state})  # 변경된 상태를 클라이언트에 전송

# --- LED 상태 요청 처리 ---
@socketio.on("get_led_status")
def handle_status_request():
    state = get_led_state()
    print(f"led 상태 : {state}")
    socketio.emit("led_status", {"state": state}) # LDE 브로드캐스트로 처리

# --- 온습도 상태 요청 처리 ---
@socketio.on("get_temperature_humidity_status")
def send_temperature_humidity_status():
    ret_temp_hum = {"temp": "N/A", "hum": "N/A"}  # 기본 응답값 설정
    if latest_temp is not None and latest_hum is not None:
        ret_temp_hum = {"temp": latest_temp, "hum": latest_hum}
    socketio.emit("temperature_humidity_status", ret_temp_hum, room=request.sid)  # 온습도 상태는 유니캐스트로 처리

# --- 센서 측정 스레드 ---
def temperature_monitor_thread():
    global latest_temp, latest_hum
    while True:
        try:
            temp = dht_device.temperature
            hum = dht_device.humidity
            if hum is not None and temp is not None:
                latest_temp = round(temp, 1)   # 소수점 1자리로 반올림하여 저장
                latest_hum = round(hum, 1)
                print(f"센서 측정: {latest_temp}℃ / {latest_hum}%")

                # MQTT 퍼블리시
                mqtt_client.publish("home/temperature", str(latest_temp))  # 온도 MQTT 토픽 전송
                mqtt_client.publish("home/humidity", str(latest_hum))  # 습도 MQTT 토픽 전송

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
