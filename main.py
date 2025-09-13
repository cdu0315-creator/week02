# main.py - FastAPI로 Arduino 제어
# ... 위쪽 생략 ...
from pyfirmata2 import Arduino, util
import time
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse

app = FastAPI(title="Arduino API")

board = Arduino("COM3")              # 실제 포트로
it = util.Iterator(board); it.start()
time.sleep(1.0)

led = board.get_pin('d:13:o')        # ✅ 여기서 '한 번만' 만들기
led.write(0)                         # 초기 꺼짐

@app.get("/", response_class=HTMLResponse)
def main_page():
    return ""

@app.post("/led/{state}")
def control_led(state: int):
    if state not in (0, 1):
        raise HTTPException(status_code=400, detail="state는 0 또는 1")
    led.write(state)                 # ✅ 엔드포인트에서는 재사용만
    return {"status": "LED 켜짐" if state == 1 else "LED 꺼짐"}
