# dashboard.py — Streamlit LED 제어 전용
import streamlit as st
import pyfirmata2
import time

# 페이지 설정
st.set_page_config(page_title="Arduino LED 제어", page_icon="💡", layout="wide")

# Arduino 연결 (세션 상태로 관리)
if "board" not in st.session_state:
    try:
        st.session_state.board = pyfirmata2.Arduino("COM3")
        it = pyfirmata2.util.Iterator(st.session_state.board)
        it.start()
        time.sleep(2)  # 초기화 대기
        st.session_state.led_pin = st.session_state.board.get_pin("d:13:o")
        st.session_state.connected = True
        st.session_state.led_state = 0  # 0=끄기, 1=켜기
    except Exception as e:
        st.session_state.connected = False
        st.session_state.error = str(e)

st.title("💡 Arduino LED 제어")

# 연결 상태 표시
if not st.session_state.get("connected", False):
    st.error("❌ Arduino 연결 실패 (포트/케이블/드라이버 확인).")
    if "error" in st.session_state:
        st.caption(f"에러: {st.session_state.error}")
    st.stop()
else:
    st.success("✅ Arduino 연결됨 (COM3)")

# 사이드바 - LED 제어만
with st.sidebar:
    st.header("🎛️ LED 제어 (D13)")
    if st.button("LED 켜기"):
        st.session_state.led_pin.write(1)
        st.session_state.led_state = 1
        st.success("LED 켜짐")

    if st.button("LED 끄기"):
        st.session_state.led_pin.write(0)
        st.session_state.led_state = 0
        st.success("LED 꺼짐")

# 현재 상태 표시
st.subheader("현재 LED 상태")
st.metric(label="D13 LED", value="켜짐" if st.session_state.led_state == 1 else "꺼짐")
