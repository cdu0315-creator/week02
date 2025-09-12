# ------------------------------------------------------------
# 아두이노 + 조도센서(LDR) + LED 제어 (pyfirmata2, 콜백 방식)
# 사전 준비:
#  1) Arduino IDE에서: File → Examples → Firmata → StandardFirmata 업로드
#  2) IDE의 Serial Monitor/Plotter는 닫아 포트 점유 해제
#  3) 배선(전압분배기):
#     - 형태 A(어두울수록 값 ↑): 5V — 10kΩ — (A0) — LDR — GND → 코드에서 v > THRESHOLD 가 어두움
#     - 형태 B(어두울수록 값 ↓): 5V — LDR — (A0) — 10kΩ — GND → 코드에서 v < THRESHOLD 가 어두움
#     (본 코드는 v > THRESHOLD 일 때 LED ON)
#  4) A0 아날로그 값 범위: 0.0 ~ 1.0
# ------------------------------------------------------------

from pyfirmata2 import Arduino
import time

PORT = 'COM3'  # 위에서 확인한 포트 번호 입력 (예: COM3, COM4 등)
THRESHOLD = 0.3  # 임계값: v가 이 값보다 크면(현재 로직) LED를 켠다

board = Arduino(PORT)             # 보드 연결(StandardFirmata가 업로드되어 있어야 함)
led = board.get_pin('d:13:o')     # D13 디지털 출력(외부 LED 또는 보드 내장 LED 제어)
a0  = board.analog[0]             # A0 아날로그 입력 핀 객체(0~1 값 전달)

# 통신 확인: 2번 점멸 (보드-PC 연결 및 핀 제어가 정상인지 빠르게 확인)
for _ in range(2):
    led.write(1); time.sleep(0.2)
    led.write(0); time.sleep(0.2)

# (선택) 샘플링 간격 설정: 일부 보드에서 아날로그 리포팅 안정화에 도움(단위 ms)
try: board.samplingOn(50)
except: pass  # 지원하지 않는 보드/펌웨어에서도 코드가 중단되지 않도록 예외 무시

def on_a0(v):
    # 콜백: A0에서 새로운 샘플이 들어올 때마다 pyfirmata2가 호출해줌
    if v is None: return          # 초기/노이즈 구간일 수 있으므로 None이면 스킵
    print(f"value={v:.3f}")       # 현재 측정값(0.000 ~ 1.000) 로그 출력
    led.write(1 if v > THRESHOLD else 0)  # 현재 로직: 값이 임계값보다 크면 LED ON

a0.register_callback(on_a0)  # 콜백 등록(값 수신 시 on_a0 호출)
a0.enable_reporting()        # 아날로그 리포팅 시작(보드→PC로 주기적 전송)
time.sleep(1.0)              # 초기 안정화 대기(센서/리포팅 시작 대기)

print("수신 중… (Ctrl+C 종료)")  # 실행 상태 안내
try:
    while True: time.sleep(0.1)  # 메인 루프는 유지만(콜백이 실질 처리)
except KeyboardInterrupt:
    pass                         # Ctrl+C로 정상 종료
finally:
    a0.disable_reporting()       # 아날로그 리포팅 중지
    board.exit()                 # 포트/리소스 해제 (다음 실행을 위해 중요)
