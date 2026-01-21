import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# 데이터 생성
n_rows = 50
base_date = datetime.now()
dates = [base_date - timedelta(days=x) for x in range(n_rows)]
agencies = ['한국전력공사 강원지사', '한국전력공사 경기북부본부', '원주시청', '강원도 교육청']

data = []
for i in range(n_rows):
    agency = np.random.choice(agencies)
    base_price = np.random.randint(50000000, 500000000)
    
    # 사정율: 98% ~ 102%
    adj_rate = np.random.normal(100.0, 0.5)
    adj_rate = np.clip(adj_rate, 97.5, 102.5)
    
    # 예정가격
    est_price = int(base_price * (adj_rate / 100))
    
    # 낙찰하한율 87.745%
    drop_limit_rate = 87.745
    bid_rate = drop_limit_rate + np.random.exponential(0.1)
    winning_price = int(est_price * (bid_rate / 100))
    
    data.append({
        '공고명': f'2024년 {agency} 노후 전선 교체 공사 제{i}호',
        '발주처': agency,
        '공고일': dates[i].strftime('%Y-%m-%d'),
        '기초금액': base_price,
        '예정가격': est_price,
        '낙찰금액': winning_price,
        '사정율': round(adj_rate, 4),
        '낙찰율': round(bid_rate, 4)
    })

df = pd.DataFrame(data)

# 엑셀 파일로 저장
output_path = 'sample_bids.xlsx'
df.to_excel(output_path, index=False)
print(f"Sample Excel file created at: {output_path}")
