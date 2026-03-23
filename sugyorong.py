import streamlit as st
import numpy as np
import plotly.graph_objects as go

# 페이지 기본 설정 (넓은 화면, 어두운 테마에 어울리는 아이콘)
st.set_page_config(page_title="차원 우주 탐색기 | Chaos Attractors", page_icon="🌌", layout="wide")

# 스타일링 (CSS를 통한 UI 개선)
st.markdown("""
<style>
    .main {
        background-color: #0E1117;
    }
    h1 {
        color: #00FFCC;
        text-shadow: 0 0 10px #00FFCC50;
    }
</style>
""", unsafe_allow_html=True)

st.title("🌌 우주적 혼돈: 3D 기묘한 끌개 탐색기")
st.markdown("""
**카오스 이론(Chaos Theory)**의 수학적 세계로 오신 것을 환영합니다. 
아래의 3D 시각화는 초기 조건의 미세한 변화가 결과에 엄청난 차이를 만드는 '나비 효과'를 시각적으로 보여줍니다. 
왼쪽의 패널에서 우주의 물리 법칙(변수)을 조작하여 자신만의 새로운 은하계를 창조해 보세요.
""")

# --- 수학적 끌개(Attractor) 함수 정의 ---
@st.cache_data
def generate_lorenz(num_steps, dt, a, b, c):
    xs, ys, zs = np.empty(num_steps), np.empty(num_steps), np.empty(num_steps)
    xs[0], ys[0], zs[0] = (0.0, 1.0, 1.05)
    for i in range(1, num_steps):
        xs[i] = xs[i-1] + (a * (ys[i-1] - xs[i-1])) * dt
        ys[i] = ys[i-1] + (xs[i-1] * (b - zs[i-1]) - ys[i-1]) * dt
        zs[i] = zs[i-1] + (xs[i-1] * ys[i-1] - c * zs[i-1]) * dt
    return xs, ys, zs

@st.cache_data
def generate_thomas(num_steps, dt, b):
    xs, ys, zs = np.empty(num_steps), np.empty(num_steps), np.empty(num_steps)
    xs[0], ys[0], zs[0] = (0.1, 0.0, 0.0)
    for i in range(1, num_steps):
        xs[i] = xs[i-1] + (np.sin(ys[i-1]) - b * xs[i-1]) * dt
        ys[i] = ys[i-1] + (np.sin(zs[i-1]) - b * ys[i-1]) * dt
        zs[i] = zs[i-1] + (np.sin(xs[i-1]) - b * zs[i-1]) * dt
    return xs, ys, zs

@st.cache_data
def generate_aizawa(num_steps, dt, a, b, c, d, e, f):
    xs, ys, zs = np.empty(num_steps), np.empty(num_steps), np.empty(num_steps)
    xs[0], ys[0], zs[0] = (0.1, 0.0, 0.0)
    for i in range(1, num_steps):
        x, y, z = xs[i-1], ys[i-1], zs[i-1]
        xs[i] = x + ((z - b) * x - d * y) * dt
        ys[i] = y + (d * x + (z - b) * y) * dt
        zs[i] = z + (c + a * z - (z**3) / 3 - (x**2 + y**2) * (1 + e * z) + f * z * (x**3)) * dt
    return xs, ys, zs

# --- 사이드바 UI 구성 ---
with st.sidebar:
    st.header("🎛️ 차원 제어 패널")
    
    attractor_type = st.selectbox(
        "은하계(끌개) 유형 선택",
        ["로렌즈 끌개 (Lorenz)", "토마스 끌개 (Thomas)", "아이자와 끌개 (Aizawa)"]
    )
    
    num_points = st.slider("입자 수 (해상도)", min_value=5000, max_value=50000, value=20000, step=5000, 
                           help="값이 클수록 멋지지만 렌더링 시간이 길어집니다.")
    
    color_map = st.selectbox(
        "스펙트럼 (색상 테마)",
        ["plasma", "inferno", "magma", "viridis", "hsv", "twilight"]
    )
    
    st.markdown("---")
    st.subheader("물리 법칙 변수 조작")
    
    # 끌개 종류에 따른 슬라이더 동적 생성
    if attractor_type == "로렌즈 끌개 (Lorenz)":
        a = st.slider("변수 A (프란틀 수)", 1.0, 20.0, 10.0)
        b = st.slider("변수 B (레일리 수)", 10.0, 50.0, 28.0)
        c = st.slider("변수 C", 1.0, 5.0, 2.667)
        xs, ys, zs = generate_lorenz(num_points, 0.01, a, b, c)
        
    elif attractor_type == "토마스 끌개 (Thomas)":
        b = st.slider("마찰 계수 (B)", 0.1, 0.3, 0.2081)
        xs, ys, zs = generate_thomas(num_points, 0.1, b)
        
    else: # Aizawa
        a = st.slider("변수 A", 0.1, 1.5, 0.95)
        b = st.slider("변수 B", 0.1, 1.5, 0.7)
        c = st.slider("변수 C", 0.1, 1.0, 0.6)
        d = st.slider("변수 D", 1.0, 5.0, 3.5)
        e = st.slider("변수 E", 0.1, 1.0, 0.25)
        f = st.slider("변수 F", 0.01, 0.5, 0.1)
        xs, ys, zs = generate_aizawa(num_points, 0.01, a, b, c, d, e, f)

# --- Plotly 3D 그래프 생성 ---
# 색상을 위한 배열 (시간의 흐름에 따라 색이 변하도록)
colors = np.arange(num_points)

fig = go.Figure(data=[go.Scatter3d(
    x=xs, y=ys, z=zs,
    mode='lines',
    line=dict(
        color=colors,
        colorscale=color_map,
        width=2
    ),
    opacity=0.8
)])

# 그래프 레이아웃 설정 (배경 투명화 및 축 숨김으로 우주 느낌 강조)
fig.update_layout(
    margin=dict(l=0, r=0, b=0, t=0),
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    scene=dict(
        xaxis=dict(showbackground=False, showticklabels=False, title=''),
        yaxis=dict(showbackground=False, showticklabels=False, title=''),
        zaxis=dict(showbackground=False, showticklabels=False, title=''),
        bgcolor='#0E1117'
    ),
    height=700
)

# 메인 화면에 그래프 출력
st.plotly_chart(fig, use_container_width=True)

# 하단 정보
st.info("💡 **팁:** 마우스로 드래그하여 3D 우주를 회전시키고, 스크롤하여 확대/축소해 보세요. 좌측 패널의 변수를 아주 조금만 바꿔도 우주의 모양이 완전히 달라집니다!")
