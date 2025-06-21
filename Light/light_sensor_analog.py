import spidev
import time
# SPI 초기화
spi = spidev.SpiDev()
spi.open(0, 0)  # bus=0, device=0: CE0
spi.max_speed_hz = 1000000  # SPI 클럭 속도 설정 (1MHz = 초당 100만 비트)
spi.mode = 0  # SPI Mode 0 (CPOL=0, CPHA=0) 설정

# MCP3208 아날로그 데이터 읽기 함수 (0~7 채널)
def read_adc(channel):
    if not 0 <= channel <= 7:
        return -1
    # MCP3208은 10비트 명령어를 3바이트로 나눠 전송합니다:
    cmd1 = 0b00000110 | ((channel & 0x04) >> 2) # 시작 비트(1) + 단일 엔드 모드(1) + 채널 상위 비트 (D2)
    cmd2 = (channel & 0x03) << 6  # 나머지 채널 비트 D1, D0 (<< 6  상위 6비트로 이동) 
    adc = spi.xfer2([cmd1, cmd2, 0]) # 3byte로 나눠서 보냄 #CH0이면 0b00000110 0b00000000 0b00000000
    print(f"Raw SPI response: {adc}")
    data = ((adc[1] & 0x0F) << 8) | adc[2]  # adc[0]: 무시, adc[1] : 결과의 상위 4비트(B11~ B8), adc[2] 결과의 상위 8비트(B7~B0)
    '''
    adc1 & 0x0F
    → 0b10101100 & 0b00001111 = 0b00001100 = 12 (10진수)

    0b00001100 << 8
    → 0b00001100_00000000 = 3072 (10진수)

    result = 3072 | 240
    → 0b00001100_11110000 = 3312
    '''
    return data
try:
    print("조도센서 값 읽기 시작...")
    print("Ctrl+C로 종료")
   
    while True:
        value = read_adc(0) 
        voltage = value * 5.0 / 4095  # VREF = 5V 기준
       
        print(f"방법 - 조도 값: {value}, 전압: {voltage:.2f}V")
        print("-" * 50)
       
        time.sleep(1)
except KeyboardInterrupt:
    print("\n프로그램 종료")
finally:
    spi.close()
    print("SPI 연결 종료")