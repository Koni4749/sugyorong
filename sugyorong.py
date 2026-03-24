import streamlit as st

# 페이지 기본 설정
st.set_page_config(page_title="차원 우주 탐색기 | Home", page_icon="🌌", layout="wide")

st.markdown("""
<style>
    .main { background-color: #0E1117; }
    h1 { color: #00FFCC; text-shadow: 0 0 10px #00FFCC50; }
</style>
""", unsafe_allow_html=True)

st.title("🌌 차원 우주 탐색 포털에 오신 것을 환영합니다!")
st.markdown("""
이곳은 다양한 수학적, 물리학적 시뮬레이션을 통해 우주의 신비를 시각화하는 웹사이트입니다.

👈 **왼쪽 사이드바 메뉴**를 클릭하여 원하는 차원으로 이동해 보세요!

* **1_chaos:** 카오스 이론에 기반한 3D 기묘한 끌개 탐색기
* **2_Spacetime:** 질량과 파동이 만드는 시공간 왜곡 엔진 시뮬레이터
""")
