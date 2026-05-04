import streamlit as st
from pathlib import Path
import tempfile

CALL_FILE = Path(tempfile.gettempdir()) / "call.txt"

st.set_page_config(
    page_title="🍱 우리학교 급식 호출 시스템",
    page_icon="🍱",
    layout="wide"
)

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


# 1학년
st.markdown("### 1학년")
col1, col2, col3 = st.columns(3)

with col1:
    st.button("1학년 1반 호출", on_click=set_call, args=("1학년 1반 식사 중",))

with col2:
    st.button("1학년 2반 호출", on_click=set_call, args=("1학년 2반 식사 중",))

with col3:
    st.button("1학년 3반 호출", on_click=set_call, args=("1학년 3반 식사 중",))

st.divider()

# 2학년 (확장 예시)
st.markdown("### 2학년")
col4, col5, col6 = st.columns(3)

with col4:
    st.button("2학년 1반 호출", on_click=set_call, args=("2학년 1반 식사 중",))

with col5:
    st.button("2학년 2반 호출", on_click=set_call, args=("2학년 2반 식사 중",))

with col6:
    st.button("2학년 3반 호출", on_click=set_call, args=("2학년 3반 식사 중",))

st.divider()

st.markdown("### 상태 초기화")
if st.button("초기화", type="secondary"):
    reset_call()
    st.success("상태가 초기화되었습니다.")
