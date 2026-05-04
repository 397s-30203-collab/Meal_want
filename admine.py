import streamlit as st
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
CALL_FILE = BASE_DIR / "call.txt"

st.title("👩‍🏫 급식 호출 관리자")

try:
    if not CALL_FILE.exists():
        CALL_FILE.write_text("대기중", encoding="utf-8")
except Exception as e:
    st.error(f"call.txt 생성 오류: {e}")
    st.stop()

if "current_call" not in st.session_state:
    try:
        st.session_state.current_call = CALL_FILE.read_text(encoding="utf-8")
    except Exception as e:
        st.session_state.current_call = "오류 발생"
        st.error(f"call.txt 읽기 오류: {e}")

st.subheader("현재 상태")
st.info(st.session_state.current_call)

st.divider()
st.subheader("반 호출")


def set_call(text: str):
    CALL_FILE.write_text(text, encoding="utf-8")
    st.session_state.current_call = text


def reset_call():
    CALL_FILE.write_text("대기중", encoding="utf-8")
    st.session_state.current_call = "대기중"

col1, col2, col3 = st.columns(3)

with col1:
    st.button("1학년 1반 호출", on_click=set_call, args=("1학년 1반 식사 중",))

with col2:
    st.button("1학년 2반 호출", on_click=set_call, args=("1학년 2반 식사 중",))

with col3:
    st.button("1학년 3반 호출", on_click=set_call, args=("1학년 3반 식사 중",))

st.button("초기화", on_click=reset_call)
