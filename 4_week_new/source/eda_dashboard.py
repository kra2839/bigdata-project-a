# eda_dashboard.py (수정 완료본)
import streamlit as st
import pandas as pd
import numpy as np

# ---- 페이지 설정 ----
st.set_page_config(page_title='기초 EDA 대시보드', layout='wide')
st.title('기초 EDA 대시보드')

# ---- 데이터 생성 ----
np.random.seed(42)
df = pd.DataFrame({
    '날짜': pd.date_range('2026-01-01', periods=100),
    '카테고리': np.random.choice(['전자제품', '의류', '식품'], 100),
    '매출': np.random.randint(100, 1000, 100),
    '고객수': np.random.randint(10, 200, 100),
    '전환율': np.random.uniform(0.01, 0.20, 100).round(4)
})

# ---- 사이드바: 필터 ----
st.sidebar.header('필터')

selected_category = st.sidebar.selectbox(
    '카테고리 선택',
    ['전체'] + list(df['카테고리'].unique())
)

data_range = st.sidebar.slider('최근 데이터 범위 (일수)', 10, 100, 50, 10)

# ---- 데이터 필터링 ----
filtered_df = df.tail(data_range)

if selected_category != '전체':
    filtered_df = filtered_df[filtered_df['카테고리'] == selected_category]

st.sidebar.write('---')
st.sidebar.write(f'필터링된 데이터: **{len(filtered_df)}행**')

# ---- 메인: 탭 구성 ----
tab1, tab2 = st.tabs(['요약 대시보드', '원본 데이터'])

# =========================
# 📊 탭1: 요약 대시보드
# =========================
with tab1:
    st.subheader('핵심 지표')

    kpi1, kpi2, kpi3 = st.columns(3)

    kpi1.metric(
        '총 매출',
        f"₩{filtered_df['매출'].sum():,}",
        f"{filtered_df['매출'].mean():.0f} (평균)"
    )

    kpi2.metric(
        '총 고객수',
        f"{filtered_df['고객수'].sum():,}명",
        f"{filtered_df['고객수'].mean():.0f} (평균)"
    )

    kpi3.metric(
        '평균 전환율',
        f"{filtered_df['전환율'].mean():.2%}",
        f"{filtered_df['전환율'].std():.2%} (표준편차)"
    )

    st.write('---')

    # 📈 매출 추이
    st.subheader('매출 추이')

    chart_data = filtered_df.groupby('날짜')['매출'].sum().reset_index()
    st.line_chart(chart_data.set_index('날짜'))

# =========================
# 📄 탭2: 원본 데이터
# =========================
with tab2:
    st.subheader('필터링된 원본 데이터')

    st.write(f'총 **{len(filtered_df)}건**의 데이터')
    st.dataframe(filtered_df, use_container_width=True, height=400)

    with st.expander('기술통계 보기'):
        st.dataframe(filtered_df.describe())