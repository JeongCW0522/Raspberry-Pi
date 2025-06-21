import threading
import time
# 전역 변수와 락 생성
counter = 0
lock = threading.Lock()  # 쓰레드 간 자원 동기화를 위한 락

# 쓰레드에서 실행할 함수 정의
def worker(name):
    global counter
    for i in range(10):
        with lock:  # 락을 사용하여 공유 자원(counter) 접근 보호
            counter += 1
            print(f"[{threading.current_thread().name}] {name} 작업 중... (카운터={counter})")
        time.sleep(1)
        
# 쓰레드 객체 생성 (target은 함수, args는 인자 튜플)
t1 = threading.Thread(target=worker, args=("스레드1",), name="Thread-1")
t2 = threading.Thread(target=worker, args=("스레드2",), name="Thread-2")

# 데몬 설정 (True로 설정 시 메인 종료와 함께 쓰레드도 종료됨, False이면 메인 종료에도 살아있음)
# 둘 다 True여야 데몬이 인정됨, 둘 중 하나만 True이면 둘 다 False인 것으로 간주됨
t1.daemon = False
t2.daemon = False

# 쓰레드 실행 -> 순차적으로 실행
t1.start()
t2.start()

# 현재 실행 중인 쓰레드 정보 출력
print(f"현재 실행 중인 쓰레드 수: {threading.active_count()}")
print(f"현재 실행 중인 쓰레드 목록: {threading.enumerate()}")

# is_alive()로 쓰레드 실행 여부 확인
print(f"{t1.name} 살아있나? {t1.is_alive()}")
print(f"{t2.name} 살아있나? {t2.is_alive()}")

# join()으로 t1과 t2 쓰레드가 종료될 때까지 메인 스레드는 대기
t1.join()
t2.join()

print("메인 쓰레드 종료됨.")
print(f"최종 카운터 값: {counter}")