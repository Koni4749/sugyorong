import streamlit as st
import numpy as np
import plotly.graph_objects as go

# --- 세션 상태 초기화 (프리셋 버튼을 위해 필요) ---
if 'p_theme' not in st.session_state: st.session_state.p_theme = "신스웨이브 (Synthwave)"
if 'p_mass' not in st.session_state: st.session_state.p_mass = 12.0
if 'p_amp' not in st.session_state: st.session_state.p_amp = 2.5
if 'p_freq' not in st.session_state: st.session_state.p_freq = 3.0
if 'p_time' not in st.session_state: st.session_state.p_time = 0.0

# --- 페이지 설정 및 CSS ---
st.set_page_config(page_title="시공간 왜곡 포탈", page_icon="🌀", layout="wide")

st.markdown("""
<style>
    .main { background-color: #050505; }
    h1 { color: #FF007A; text-shadow: 0 0 15px #FF007A80; font-family: 'Courier New', Courier, monospace;}
    h3 { color: #00E5FF; }
    .stButton>button { width: 100%; border-radius: 5px; border: 1px solid #00E5FF; color: #00E5FF; background-color: transparent; }
    .stButton>button:hover { background-color: #00E5FF30; border-color: #FF007A; color: #FF007A; }
</style>
""", unsafe_allow_html=True)

# --- 헤더 섹션 ---
st.title("🌀 사이버 매트릭스: 시공간 왜곡 엔진")
st.markdown("""
이곳은 질량과 파동이 만나 3차원 공간을 찢고 휘게 만드는 **가상 시공간 시뮬레이터**입니다. 
아래의 프리셋 버튼을 클릭하거나, 좌측 패널에서 직접 우주의 물리 법칙을 조작하여 아름다운 형상을 빚어내 보세요.
""")

# --- 프리셋 버튼 ---
st.markdown("### 텔레포트 프리셋 (원클릭 우주 생성)")
col1, col2, col3, col4 = st.columns(4)

def set_preset(preset):
    if preset == "블랙홀":
        st.session_state.p_mass = 20.0; st.session_state.p_amp = 0.5; st.session_state.p_freq = 1.0; st.session_state.p_theme = "적색 거성 (Red Giant)"
    elif preset == "웜홀":
        st.session_state.p_mass = -18.0; st.session_state.p_amp = 4.0; st.session_state.p_freq = -2.5; st.session_state.p_theme = "신스웨이브 (Synthwave)"
    elif preset == "양자 요동":
        st.session_state.p_mass = 0.0; st.session_state.p_amp = 8.0; st.session_state.p_freq = 5.0; st.session_state.p_theme = "사이버 매트릭스 (Cyber Matrix)"
    elif preset == "잔잔한 우주":
        st.session_state.p_mass = 2.0; st.session_state.p_amp = 1.0; st.session_state.p_freq = 2.0; st.session_state.p_theme = "은하수 (Milky Way)"

with col1:
    if st.button("🌌 심연의 블랙홀"): set_preset("블랙홀")
with col2:
    if st.button("🌀 다차원 웜홀"): set_preset("웜홀")
with col3:
    if st.button("⚛️ 양자 요동 (격변)"): set_preset("양자 요동")
with col4:
    if st.button("🌊 잔잔한 우주"): set_preset("잔잔한 우주")

# --- 커스텀 컬러맵 정의 ---
custom_scales = {
    "신스웨이브 (Synthwave)": [[0.0, '#0d0221'], [0.3, '#4a0072'], [0.6, '#ff007a'], [0.85, '#00e5ff'], [1.0, '#ffffff']],
    "사이버 매트릭스 (Cyber Matrix)": [[0.0, '#000000'], [0.4, '#003300'], [0.8, '#00ff00'], [1.0, '#ccffcc']],
    "적색 거성 (Red Giant)": [[0.0, '#1a0000'], [0.4, '#8b0000'], [0.7, '#ff4500'], [1.0, '#ffffaa']],
    "은하수 (Milky Way)": [[0.0, '#000022'], [0.5, '#4b0082'], [0.8, '#8a2be2'], [1.0, '#e6e6fa']]
}

# --- 사이드바 제어판 ---
with st.sidebar:
    st.header("🎛️ 차원 제어 콘솔")
    
    st.selectbox("스펙트럼 필터 (색상)", list(custom_scales.keys()), key='p_theme')
    
    st.markdown("---")
    st.subheader("물리 엔진 조작")
    st.slider("중력 질량 (Mass)", min_value=-25.0, max_value=25.0, step=0.5, key='p_mass',
              help="양수(+)는 공간을 아래로 파이게(블랙홀) 하고, 음수(-)는 솟아오르게(화이트홀) 합니다.")
    
    st.slider("파동 진폭 (Energy)", min_value=0.0, max_value=10.0, step=0.5, key='p_amp',
              help="주변으로 퍼져나가는 중력파의 높이를 결정합니다.")
    
    st.slider("파동 주파수 (Frequency)", min_value=-5.0, max_value=10.0, step=0.5, key='p_freq',
              help="파동이 얼마나 촘촘하게 퍼질지 결정합니다.")
    
    st.markdown("---")
    st.subheader("⏱️ 시간 제어 (Time Control)")
    st.slider("시간의 흐름 드래그하기", min_value=0.0, max_value=20.0, step=0.2, key='p_time',
              help="마우스로 이 슬라이더를 잡고 좌우로 빠르게 드래그 해보세요! 파동이 살아 숨쉬는 것처럼 움직입니다.")
    
    res = st.slider("렌더링 해상도", min_value=50, max_value=150, value=100, step=10)

# --- 수학적 시공간 지형 생성 ---
@st.cache_data(show_spinner=False)
def generate_spacetime(mass, amp, freq, time, resolution):
    x = np.linspace(-10, 10, resolution)
    y = np.linspace(-10, 10, resolution)
    X, Y = np.meshgrid(x, y)
    
    # 원점으로부터의 거리 (0으로 나누는 것을 방지하기 위해 0.5 추가)
    R = np.sqrt(X**2 + Y**2) + 0.5 
    
    # 1. 중력 우물 (Gravity Well) - 중심부 시공간 왜곡
    Z_gravity = -(mass / R) * np.exp(-R/5) 
    
    # 2. 중력파 (Gravitational Waves) - 퍼져나가는 물결
    Z_waves = amp * np.sin(freq * R - time) * np.exp(-R/10)
    
    # 3. 양자 격자 텍스처 (Quantum Grid) - 표면의 미세한 사이버네틱 무늬
    Z_grid = 0.5 * np.sin(X*2) * np.cos(Y*2) * np.exp(-R/8)
    
    # 최종 시공간(Z) 합산 및 극한값 자르기 (그래프가 너무 뾰족해지는 것 방지)
    Z_total = Z_gravity + Z_waves + Z_grid
    Z_total = np.clip(Z_total, -15, 15)
    
    return X, Y, Z_total

X, Y, Z = generate_spacetime(st.session_state.p_mass, st.session_state.p_amp, 
                             st.session_state.p_freq, st.session_state.p_time, res)

# --- Plotly 3D Surface 렌더링 ---
colorscale = custom_scales[st.session_state.p_theme]

fig = go.Figure(data=[go.Surface(
    x=X, y=Y, z=Z,
    colorscale=colorscale,
    showscale=False, # 옆에 뜨는 컬러바 숨김
    lighting=dict(ambient=0.6, diffuse=0.8, roughness=0.1, specular=1.2, fresnel=0.2), # 광원 반사 효과 극대화
    contours_z=dict(show=True, usecolormap=True, highlightcolor="white", project_z=True) # 바닥에 그림자 윤곽선 투영
)])

# 축 숨기기 및 배경 투명화 처리
fig.update_layout(
    margin=dict(l=0, r=0, b=0, t=0),
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    scene=dict(
        xaxis=dict(showbackground=False, visible=False),
        yaxis=dict(showbackground=False, visible=False),
        zaxis=dict(showbackground=False, visible=False),
        camera=dict(eye=dict(x=1.2, y=1.2, z=0.6)) # 초기 카메라 각도
    ),
    height=600
)

st.plotly_chart(fig, use_container_width=True)

# --- 수식 설명 (하단) ---
with st.expander("🔬 이 지형을 만들어낸 물리학(수학) 공식 보기"):
    st.markdown("이 3D 표면은 아래의 세 가지 수학적 방정식이 중첩되어 실시간으로 계산된 결과물입니다.")
    st.latex(r"Z(r, x, y, t) = \underbrace{-\frac{M}{r} e^{-\frac{r}{5}}}_{\text{Gravity Well}} + \underbrace{A \sin(k \cdot r - t) e^{-\frac{r}{10}}}_{\text{Gravitational Waves}} + \underbrace{0.5 \sin(2x)\cos(2y) e^{-\frac{r}{8}}}_{\text{Quantum Grid Texture}}")
    st.markdown("*( $M$=질량, $A$=파동 진폭, $k$=파동 주파수, $t$=시간, $r$=중심으로부터의 거리 )*")
