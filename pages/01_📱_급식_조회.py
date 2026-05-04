import streamlit as st
import requests
from datetime import datetime
from pathlib import Path
import tempfile

CALL_FILE = Path(tempfile.gettempdir()) / "call.txt"

@st.cache_data(ttl=600)
def fetch_menu(key: str, atpt: str, schul: str, date: str):
    url = (
        f"https://open.neis.go.kr/hub/mealServiceDietInfo?KEY={key}&Type=json"
        f"&ATPT_OFCDC_SC_CODE={atpt}&SD_SCHUL_CODE={schul}&MLSV_YMD={date}"
    )
    res = requests.get(url, timeout=5)
    res.raise_for_status()
    return res.json()

st.set_page_config(
    page_title="🍱 우리학교 급식 호출 시스템",
    page_icon="🍱",
    layout="wide"
)

st.title("📱 급식 조회")

today = datetime.today().strftime("%Y%m%d")

KEY = "55a38ff473224d2090f4dfc7a0300ed9"
ATPT = "M10"
SCHUL = "8000069"

col1, col2 = st.columns(2)

with col1:
    st.subheader("🍱 오늘 급식")
    
    if KEY == "여기에_API키":
        st.warning("API 키를 설정하세요. 급식 정보는 표시되지 않습니다.")
    else:
        try:
            data = fetch_menu(KEY, ATPT, SCHUL, today)
            meal_info = data.get('mealServiceDietInfo')

            if not meal_info or len(meal_info) < 2:
                st.warning("오늘 급식 정보 없음")
            else:
                rows = meal_info[1].get('row')
                if not rows:
                    st.warning("오늘 급식 정보 없음")
                else:
                    menu = rows[0].get('DDISH_NM', '')
                    if not menu:
                        st.warning("오늘 급식 정보 없음")
                    else:
                        menu = menu.replace("<br/>", "\n")
                        st.text(menu)
        except Exception as e:
            st.warning("오늘 급식 정보 없음")
            st.info(f"상세 오류: {e}")

with col2:
    st.subheader("🔔 현재 호출 반")
    
    # call.txt 자동 생성
    try:
        if not CALL_FILE.exists():
            CALL_FILE.write_text("대기중", encoding="utf-8")
    except Exception as e:
        st.error(f"call.txt 생성 오류: {e}")
        st.stop()

    try:
        current_call = CALL_FILE.read_text(encoding="utf-8")
    except Exception as e:
        st.error(f"call.txt 읽기 오류: {e}")
        current_call = "오류 발생"

    st.success(current_call)
    
    if st.button("🔄 새로고침"):
        st.rerun()
