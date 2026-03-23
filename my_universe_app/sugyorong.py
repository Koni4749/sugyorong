import streamlit as st

# 페이지 설정
st.set_page_config(page_title="Sugyorong Multiverse", page_icon="🌌", layout="centered")

# 배경 및 폰트 스타일링
st.markdown("""
<style>
    .main { background-color: #000000; }
    h1 { color: #00E5FF; text-shadow: 0 0 20px #00E5FF80; text-align: center; font-size: 3.5rem; }
    .portal-text { color: #E0E0E0; text-align: center; font-size: 1.2rem; line-height: 1.8; }
    .highlight { color: #FF007A; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

st.title("🌌 Sugyorong Multiverse")

st.markdown("""
<div class="portal-text">
<br>
환영합니다. 이곳은 <span class="highlight">Sugyorong</span> 님이 창조한 <b>차원 간 이동 포탈</b>입니다.<br>
수학적 카오스와 물리적 시공간의 왜곡을 실시간으로 렌더링하고 탐험할 수 있습니다.<br><br>
<b>왼쪽 사이드바 메뉴를 열어 탐색할 차원을 선택하세요.</b>
</div>
""", unsafe_allow_html=True)

# 신비로운 우주 이미지 삽입
st.image("https://images.unsplash.com/photo-1462331940025-496dfbfc7564?auto=format&fit=crop&w=800&q=80", caption="Welcome to the Multiverse")

st.markdown("---")
st.info("💡 **시스템 메시지:** 좌측 패널의 메뉴를 클릭하여 '카오스 끌개'나 '시공간 왜곡 엔진'을 가동하십시오.")
