import pandas as pd
import numpy as np
from datetime import datetime

# 1. 크롤링된 실제 데이터 (3건)
crawled_data = [
  {
    "공고명": "2026년도 상수도과 업무용 공용차량(전기차) 임차 용역",
    "개찰일시": "2026/01/21 11:09:27",
    "기초금액": "59,290,000 원",
    "예정가격": "58,286,875 원",
    "낙찰금액": "52,344,600 원",
    "낙찰하한율": "87.745% (추정)",
    "투찰률": "89.805%"
  },
  {
    "공고명": "강북 관내 유·중등 전기시설물 유지보수 단가계약",
    "개찰일시": "2026/01/21 11:11:35",
    "기초금액": "109,967,000 원",
    "예정가격": "109,246,225 원",
    "낙찰금액": "98,530,390 원",
    "낙찰하한율": "87.745% (추정)",
    "투찰률": "90.191%"
  },
  {
    "공고명": "디지털관 외 2동 로비 개선 공사(전기)",
    "개찰일시": "2026/01/21 11:17:58",
    "기초금액": "26,961,000 원",
    "예정가격": "26,929,750 원",
    "낙찰금액": "23,629,629 원",
    "낙찰하한율": "87.745%",
    "투찰률": "87.745%"
  }
]

def clean_money(s):
    return int(str(s).replace(',', '').replace(' 원', ''))

def clean_rate(s):
    return float(str(s).split('%')[0])

real_rows = []
for item in crawled_data:
    row = {
        '공고명': item['공고명'],
        '발주처': '실제 크롤링 데이터', # 발주처 정보가 없어서 임의 표시
        '공고일': item['개찰일시'].split(' ')[0],
        '기초금액': clean_money(item['기초금액']),
        '예정가격': clean_money(item['예정가격']),
        '낙찰금액': clean_money(item['낙찰금액']),
        '낙찰하한율': clean_rate(item['낙찰하한율']),
        '낙찰률': clean_rate(item['투찰률'])
    }
    # 사정율 계산
    if row['기초금액'] > 0:
        row['사정율'] = (row['예정가격'] / row['기초금액']) * 100
    
    real_rows.append(row)

# 2. 가상 데이터 로드 (기존 스크립트 활용 또는 재생성)
# 여기서는 파일에서 읽거나 새로 생성
from generate_realistic_data import generate_realistic_data
mock_df = generate_realistic_data(n_rows=100)
# 컬럼명 통일
# generate_realistic_data creates: '입찰공고명', '공고기관명', '개찰일시', ...
# We need to rename mock_df to match our simple schema or vice versa.
# data_loader.py expects: 공고명, 발주처, 기초금액, 사정율...

# Map mock_df to standard names
mock_df = mock_df.rename(columns={
    '입찰공고명': '공고명',
    '공고기관명': '발주처',
    '개찰일시': '공고일'
})
# Process dates in mock_df (it's string 'YYYY-MM-DD HH:MM')
mock_df['공고일'] = mock_df['공고일'].astype(str).str.split(' ').str[0]

# 3. 합치기
real_df = pd.DataFrame(real_rows)
combined_df = pd.concat([real_df, mock_df], ignore_index=True)

# 4. 저장
output_file = "2024_전기공사_통합데이터.xlsx"
combined_df.to_excel(output_file, index=False)
print(f"Created {output_file} with {len(combined_df)} rows")
