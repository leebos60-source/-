import pandas as pd
import numpy as np
from datetime import datetime, timedelta

class MockDataLoader:
    """
    개발 및 시연을 위한 가상 데이터 로더
    """
    def generate_mock_bids(self, n_rows=100):
        """
        가상의 입찰 데이터 생성
        """
        np.random.seed(42)  # 재현성을 위해 시드 고정
        
        # 날짜 생성 (최근 1년)
        base_date = datetime.now()
        dates = [base_date - timedelta(days=x) for x in range(n_rows)]
        
        data = []
        
        # 발주처 목록
        agencies = ['한국전력공사 강원지사', '한국전력공사 경기북부본부', '원주시청', '강원도 교육청']
        
        for i in range(n_rows):
            agency = np.random.choice(agencies)
            
            # 기초금액 (5천만원 ~ 5억원)
            base_price = np.random.randint(50000000, 500000000)
            
            # 사정율 생성 (98% ~ 102% 사이, 정규분포 따르도록)
            # 평균 100%, 표준편차 0.5%
            adj_rate = np.random.normal(100.0, 0.5)
            # Clip to realistic bounds
            adj_rate = np.clip(adj_rate, 97.5, 102.5)
            
            # 예정가격 = 기초금액 * (사정율 / 100)
            est_price = int(base_price * (adj_rate / 100))
            
            # 낙찰하한율 (87.745% 가정)
            drop_limit_rate = 87.745
            
            # 낙찰율 (낙찰하한율보다 살짝 높게 형성)
            bid_rate = drop_limit_rate + np.random.exponential(0.1)
            winning_price = int(est_price * (bid_rate / 100))
            
            data.append({
                '공고명': f'202{i%5}년 {agency} 전기공사 제{i}호',
                '공고일': dates[i].strftime('%Y-%m-%d'),
                '발주처': agency,
                '기초금액': base_price,
                '예정가격': est_price,
                '낙찰금액': winning_price,
                '사정율': round(adj_rate, 4), # 실제로는 역산해야 하지만 mock에서는 생성값 사용
                '낙찰율': round(bid_rate, 4)
            })
            
        return pd.DataFrame(data)

    def get_agency_stats(self, df, agency_name=None):
        if agency_name and agency_name != "전체":
            df = df[df['발주처'] == agency_name]
        return df

class FileDataLoader:
    """
    사용자가 업로드한 엑셀/CSV 데이터를 처리하는 로더
    """
    def load_from_file(self, uploaded_file):
        """
        Streamlit UploadedFile 객체를 받아 DataFrame으로 변환
        """
        try:
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file, engine='openpyxl')
            
            return self._preprocess_data(df)
        except Exception as e:
            raise ValueError(f"파일을 읽는 중 오류가 발생했습니다: {str(e)}")

    def _preprocess_data(self, df):
        """
        데이터 전처리 및 컬럼 표준화
        """
        # 필수 컬럼 매핑 (사용자 파일의 컬럼명을 표준 컬럼명으로 변환 시도)
        column_mapping = {
            '공고명': ['공사명', '입찰건명', '건명'],
            '발주처': ['공고기관', '수요기관', '기관명'],
            '기초금액': ['설계금액', '추정가격'], # 정확히는 다르지만 근사치로 사용 가능성 
            '공고일': ['입찰공고일', '게시일'],
            '예정가격': ['예가', '예비가격'],
            '낙찰금액': ['투찰금액', '낙찰가'],
            '사정율': ['사정률', '예가율', '사정율(%)'],
            '낙찰율': ['낙찰하한율', '투찰률'] # 주의: 낙찰하한율과 낙찰률은 다름
        }
        
        # 컬럼 이름 변경
        new_columns = {}
        for standard, equivalents in column_mapping.items():
            if standard in df.columns:
                continue
            for eq in equivalents:
                if eq in df.columns:
                    new_columns[eq] = standard
                    break
        
        df = df.rename(columns=new_columns)
        
        # 필수 컬럼 확인
        required_cols = ['공고명', '발주처', '기초금액'] # 최소한의 분석을 위한 필수
        missing = [col for col in required_cols if col not in df.columns]
        
        if missing:
             # 사정율이 없다면? 예정가격이라도 있어야 함
             if '사정율' not in df.columns and ('예정가격' not in df.columns or '기초금액' not in df.columns):
                 raise ValueError(f"필수 컬럼이 누락되었습니다: {', '.join(missing)}. '사정율' 또는 '예정가격' 정보가 반드시 필요합니다.")

        # 숫자 데이터 정제 (콤마 제거 등)
        numeric_cols = ['기초금액', '예정가격', '낙찰금액', '사정율', '낙찰율']
        for col in numeric_cols:
            if col in df.columns:
                # 문자열인 경우에만 처리
                if df[col].dtype == object:
                    df[col] = df[col].astype(str).str.replace(',', '').str.replace('%', '')
                    df[col] = pd.to_numeric(df[col], errors='coerce')

        # 사정율 계산 (만약 없고 예정가격/기초금액이 있다면)
        if '사정율' not in df.columns and '예정가격' in df.columns and '기초금액' in df.columns:
            df['사정율'] = (df['예정가격'] / df['기초금액']) * 100

        # 데이터 분석을 위해 사정율이 있는 행만 남김
        if '사정율' in df.columns:
             df = df.dropna(subset=['사정율'])

        return df
