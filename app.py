import streamlit as st
import numpy as np
import plotly.graph_objects as go

# 1. 페이지 레이아웃 설정
st.set_page_config(page_title="행성 궤도 시각화", page_icon="🪐", layout="centered")

st.title("🪐 천체 기하학: 행성 궤도 시각화 프로그램")
st.write("원하는 행성을 선택하면 태양을 중심으로 하는 공전 궤도를 계산하고 시각화합니다.")
st.markdown("---")

# 2. 행성 데이터 정의 (거리 단위: AU, 공전 주기 단위: 년)
# AU(Astronomical Unit): 지구와 태양 사이의 평균 거리 = 1.0
planet_db = {
    "수성 (Mercury)": {"r": 0.39, "period": 0.24, "color": "gray"},
    "금성 (Venus)": {"r": 0.72, "period": 0.62, "color": "orange"},
    "지구 (Earth)": {"r": 1.00, "period": 1.00, "color": "#1f77b4"}, # 파란색
    "화성 (Mars)": {"r": 1.52, "period": 1.88, "color": "#d62728"}   # 빨간색
}

# 3. 사용자 입력 (행성 선택)
selected_planet = st.selectbox("궤도를 확인할 행성을 선택하세요:", list(planet_db.keys()))

# 선택된 행성의 물리 데이터 추출
r = planet_db[selected_planet]["r"]
period = planet_db[selected_planet]["period"]
color = planet_db[selected_planet]["color"]

# 4. 시간 흐름 제어 슬라이더 (공전 애니메이션 대용)
time = st.slider("시간 경과를 조절해보세요 (단위: 년)", min_value=0.0, max_value=3.0, value=0.0, step=0.05)

# 5. 궤도 기하학 계산 (삼각함수 활용)
# 0부터 2*pi까지 200개의 점을 찍어 완벽한 원(궤도)을 만듭니다.
theta = np.linspace(0, 2 * np.pi, 200)
orbit_x = r * np.cos(theta)
orbit_y = r * np.sin(theta)

# 시간에 따른 현재 행성의 위치 계산 (각속도 omega = 2*pi / 주기)
current_theta = (2 * np.pi / period) * time
planet_x = r * np.cos(current_theta)
planet_y = r * np.sin(current_theta)

# 6. Plotly를 이용한 2D 우주 좌표계 시각화
fig = go.Figure()

# ① 중심에 태양 생성 (0, 0)
fig.add_trace(go.Scatter(
    x=[0], y=[0],
    mode='markers+text',
    marker=dict(size=25, color='yellow', line=dict(width=3, color='orange')),
    name='태양 (Sun)',
    text=['태양'], textposition='top center'
))

# ② 행성이 지나가는 공전 궤도(점선) 그리기
fig.add_trace(go.Scatter(
    x=orbit_x, y=orbit_y,
    mode='lines',
    line=dict(color='rgba(255, 255, 255, 0.4)', width=1.5, dash='dash'),
    name=f'{selected_planet} 궤도 경로'
))

# ③ 현재 행성의 위치에 점 찍기
fig.add_trace(go.Scatter(
    x=[planet_x], y=[planet_y],
    mode='markers+text',
    marker=dict(size=14, color=color),
    name=selected_planet,
    text=[selected_planet.split()[0]], textposition='top center'
))

# ④ 그래프 스타일 및 기하학적 비율 유지 설정
# (가로세로 비율이 1:1이어야 궤도가 찌그러지지 않고 예쁜 원으로 보입니다)
max_boundary = 1.8  # 화성 궤도(1.52)까지 예쁘게 담기 위한 최대 화면 크기
fig.update_layout(
    template="plotly_dark", # 우주 느낌을 내기 위한 다크 모드
    width=600,
    height=600,
    xaxis=dict(title="X 좌표 (AU)", range=[-max_boundary, max_boundary], scaleratio=1, scaleanchor="y"),
    yaxis=dict(title="Y 좌표 (AU)", range=[-max_boundary, max_boundary]),
    showlegend=True,
    margin=dict(l=20, r=20, t=40, b=20)
)

# 스트림릿 화면에 그래프 뿌리기
st.plotly_chart(fig)

# 7. 하단에 기하학적 계산 데이터 메트릭으로 표시
st.markdown("---")
st.subheader("📊 궤도 계산 결과 데이터")
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(label="태양과의 평균 거리 (반지름)", value=f"{r} AU")
with col2:
    st.metric(label="공전 주기 (태양 한바퀴)", value=f"{period} 년")
with col3:
    # 현재 x, y 좌표 표시
    st.metric(label="현재 행성 위치 (X, Y)", value=f"({planet_x:.2f}, {planet_y:.2f})")

st.caption("※ 본 프로그램은 계산의 편의를 위해 타원 궤도가 아닌 원 궤도로 단순화하여 계산했습니다.")
