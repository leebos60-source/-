import pandas as pd
import numpy as np

def analyze_discrepancy():
    file_path = '2024_전기공사_통합데이터.xlsx'
    
    try:
        df = pd.read_excel(file_path)
    except Exception as e:
        print(f"파일을 읽을 수 없습니다: {e}")
        return

    # 데이터 분류
    # '발주처'가 가상 데이터 생성기에 있는 목록(한전강원 등)이면 '가상', 아니면 '실제'로 추정
    # 더 확실한 방법: '비고' 컬럼이 있거나, '공고명' 패턴으로 구분
    # 여기서는 '공고명'이 "202x년 ..." 패턴이면 가상일 확률이 높음 (하지만 실제도 그럴 수 있음)
    # 가장 확실한 구분: 우리가 수동으로 추가한 애들은 '기초금액'이나 '비고'란에 흔적이 있음.
    # 하지만 파일에 '비고'가 없는 경우도 있으니...
    
    # 전략: 최근 추가한 31건(실제) vs 나머지 100건(가상)으로 분리 (행 번호 기준)
    # 왜냐하면 가상 데이터를 먼저 만들고(0~99), 뒤에 실제 데이터를 붙였기 때문(100~130)
    
    # 1. 가상 데이터 (앞쪽 100개)
    mock_df = df.iloc[:100]
    
    # 2. 실제 데이터 (100번 이후)
    real_df = df.iloc[100:]
    
    if len(real_df) == 0:
        print("실제 데이터가 아직 충분히 분류되지 않았습니다.")
        return

    print(f"--- [데이터 괴리율 분석 리포트] ---")
    print(f"■ 샘플 수: 가상({len(mock_df)}건) vs 실제({len(real_df)}건)\n")
    
    # 사정율 비교
    mock_adj = mock_df['사정율']
    real_adj = real_df['사정율']
    
    stats = pd.DataFrame({
        '구분': ['평균(Mean)', '중앙값(Median)', '표준편차(Std)', '최저(Min)', '최고(Max)'],
        '가상 데이터': [
            mock_adj.mean(), mock_adj.median(), mock_adj.std(), mock_adj.min(), mock_adj.max()
        ],
        '실제 데이터(User)': [
            real_adj.mean(), real_adj.median(), real_adj.std(), real_adj.min(), real_adj.max()
        ]
    }).set_index('구분')
    
    # 소수점 포맷팅
    pd.options.display.float_format = '{:.4f}'.format
    print(stats)
    
    print("\n--- [분석 결과 요약] ---")
    diff_mean = real_adj.mean() - mock_adj.mean()
    print(f"1. 평균 차이: 실제 데이터가 가상보다 약 {diff_mean:.4f}%p {'높습니다' if diff_mean > 0 else '낮습니다'}.")
    
    diff_std = real_adj.std() - mock_adj.std()
    print(f"2. 변동성 차이: 실제 데이터가 가상보다 퍼짐 정도가 {abs(diff_std):.4f} 만큼 {'큽니다' if diff_std > 0 else '작습니다'}.")
    
    if abs(diff_mean) < 0.5 and abs(diff_std) < 0.5:
        print("=> Conclusion: Mock data is similar to real data.")
    else:
        print("=> Conclusion: Significant difference found. Mock data logic needs tuning.")

if __name__ == "__main__":
    analyze_discrepancy()
