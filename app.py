import streamlit as st
import pandas as pd
import plotly.express as px
from data_loader import MockDataLoader, FileDataLoader
from analyzer import Analyzer

# 페이지 설정 (넓은 레이아웃)
st.set_page_config(page_title="공사 입찰가 예측 도우미", layout="wide")

# CSS로 폰트 크기 키우기 (어르신용)
st.markdown("""
    <style>
    .big-font {
        font-size:20px !important;
        font-weight: 500;
    }
    .header-text {
        font-size:32px !important;
        font-weight: bold;
        color: #1E3A8A;
    }
    .result-box {
        background-color: #f0f2f6;
        color: #333333;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #1E3A8A;
        margin-bottom: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<p class="header-text">🏗️ 공사 입찰가 예측 도우미</p>', unsafe_allow_html=True)
st.markdown('<p class="big-font">아버님, 지난 공사 데이터들을 분석해서 낙찰 확률이 높은 금액을 알려드려요.</p>', unsafe_allow_html=True)

# 사이드바 (설정)
with st.sidebar:
    st.header("📋 설정")
    
    # 데이터 로드 (우리가 만든 통합 데이터만 사용)
    @st.cache_data
    def load_data():
        import os
        local_file = '2024_전기공사_통합데이터.xlsx'
        
        # 1. 파일이 있으면 로드
        if os.path.exists(local_file):
            try:
                return pd.read_excel(local_file)
            except Exception as e:
                st.error(f"데이터 파일 로드 중 오류: {e}")
                return None
        
        # 2. 파일이 없으면 (배포 시 누락 등) 대비용 가상 데이터
        loader = MockDataLoader()
        return loader.generate_mock_bids()

    df = load_data()

    if df is not None:
        selected_agency = st.selectbox(
            "분석할 발주처를 선택하세요:",
            ["전체"] + list(df['발주처'].unique())
        )
        st.info(f"💡 분석 대상: 총 {len(df)}건의 데이터가 준비되어 있습니다.")
    else:
        selected_agency = "전체"
        st.error("데이터 파일을 찾을 수 없습니다. (2024_전기공사_통합데이터.xlsx)")

analyzer = Analyzer()

if df is not None:
    # 메인 기능 탭
    tab1, tab2 = st.tabs(["💰 입찰가 계산하기", "📊 지난 공사 분석"])
    
    with tab1:
        st.markdown("### 1. 이번 공사의 기초금액을 입력하세요")
        
        col1, col2 = st.columns([1, 2])
        with col1:
            base_price_input = st.number_input(
                "기초금액 (원)", 
                min_value=0, 
                value=100000000, 
                step=1000000,
                format="%d"
            )
        
        if st.button("계산하기 🚀", use_container_width=True, type="primary"):
            # 분석 대상 데이터 필터링
            filtered_df = df
            if selected_agency != "전체":
                filtered_df = df[df['발주처'] == selected_agency]
                
            recommendations = analyzer.calculate_winning_probability_ranges(filtered_df, base_price_input)
            
            st.markdown("### 2. 추천 입찰 금액입니다")
        
            # 데이터 건수 확인 및 경고
            if len(filtered_df) < 30:
                st.warning(f"⚠️ 경고: 현재 분석 대상 데이터가 {len(filtered_df)}건 뿐입니다. "
                           "통계적 신뢰도를 위해 최소 30건, 권장 100건 이상의 데이터가 필요합니다. "
                           "결과는 참고만 해주세요.")
            
            st.markdown("지난 기록을 봤을 때, **가장 많이 낙찰된 사정율 구간**을 기준으로 계산했습니다.")
            
            cols = st.columns(3)
            for i, rec in enumerate(recommendations):
                with cols[i]:
                    st.markdown(f"""
                    <div class="result-box">
                        <h4>#{i+1} 추천 (사정율 {rec['adj_rate']:.3f}%)</h4>
                        <h2 style='color: #d32f2f;'>{rec['bid_price']:,} 원</h2>
                        <p>과거 {rec['count']}번 이 구간에서 나옴</p>
                    </div>
                    """, unsafe_allow_html=True)
    
    with tab2:
        filtered_df = df
        if selected_agency != "전체":
            filtered_df = df[df['발주처'] == selected_agency]
            
        st.markdown(f"### {selected_agency}의 사정율 분포")
        st.write(f"총 {len(filtered_df)}건의 지난 공사 데이터를 분석했습니다.")
        
        # 히스토그램 그리기
        fig = px.histogram(
            filtered_df, 
            x="사정율", 
            nbins=30, 
            title=f"{selected_agency} 사정율 분포도",
            labels={'사정율': '사정율 (%)', 'count': '발생 횟수'},
            color_discrete_sequence=['#1E3A8A']
        )
        fig.add_vline(x=100.0, line_dash="dash", line_color="red", annotation_text="기준 100%")
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("### 📋 최근 낙찰 기록")
        st.dataframe(
            filtered_df[['공고일', '공고명', '기초금액', '낙찰금액', '사정율', '낙찰율']].sort_values('공고일', ascending=False),
            hide_index=True
        )
else:
    st.info("👈 왼쪽에서 '샘플 데이터 사용'을 선택하거나 엑셀 파일을 업로드해주세요.")

    
