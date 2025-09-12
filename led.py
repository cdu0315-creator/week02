# LED 기본 예제 (깜빡임) - pyfirmata2
import time
from pyfirmata2 import Arduino  # ← pyfirmata2 사용

# Arduino 연결
PORT = 'COM3'  # 자동 탐지 원하면: Arduino.AUTODETECT
board = Arduino(PORT)

# LED 핀 설정 (D13, 출력)
led = board.get_pin('d:13:o')

print("LED 깜빡임 테스트 (pyfirmata2)")

# 무한 반복
try:
    while True:
        led.write(1)        # LED 켜기
        print("LED ON")
        time.sleep(1)       # 1초 대기

        led.write(0)        # LED 끄기
        print("LED OFF")
        time.sleep(1)       # 1초 대기
except KeyboardInterrupt:
    print("종료합니다.")
finally:
    board.exit()            # 포트 정리
