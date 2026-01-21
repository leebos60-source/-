import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def generate_realistic_data(n_rows=300):
    # 랜덤 시드 설정
    np.random.seed(2024)
    
    # 1. 날짜 생성 (최근 1년)
    base_date = datetime.now()
    dates = [base_date - timedelta(days=np.random.randint(0, 365)) for _ in range(n_rows)]
    dates.sort(reverse=True)
    
    # 2. 발주처 및 공사명 데이터 베이스
    agencies = [
        ('강원도 원주시', '원주시청'), 
        ('한국전력공사 강원지사', '한전강원'),
        ('강원도 춘천시', '춘천시청'),
        ('강원도 교육청', '강원교육청'),
        ('한국도로공사 강원본부', '도로공사'),
        ('강원도 강릉시', '강릉시청')
    ]
    
    work_types = ['노후 전선 교체 공사', '가로등 보수 공사', '마을회관 전기 증설 공사', '공영주차장 조명 설치', '학교 LED 교체 사업', '배전선로 이설 공사']
    
    data = []
    
    for i in range(n_rows):
        # Fix: choice only accepts 1-D array, so we pick index first
        agency_idx = np.random.choice(len(agencies), p=[0.3, 0.3, 0.1, 0.1, 0.1, 0.1])
        agency_full, agency_short = agencies[agency_idx]
        
        work = np.random.choice(work_types)
        title = f"2024년 {agency_short} {work} (제{2024000+i}호)"
        
        # 3. 금액 생성 (3천만원 ~ 5억원)
        base_price = np.random.randint(3000, 50000) * 10000 
        
        # 4. 사정율 로직 (중요: 실제 분포 흉내)
        # 보통 99.5% ~ 100.5% 사이에 많이 몰림, 가끔 튀는 값
        if np.random.random() < 0.8:
            adj_rate_raw = np.random.normal(100.0, 0.2) # 중심부
        else:
            adj_rate_raw = np.random.normal(100.0, 0.8) # 넓은 분포
            
        adj_rate = np.clip(adj_rate_raw, 97.5, 102.5)
        
        # 5. 예정가격 (기초금액 * 사정율)
        # 실제로는 원단위 절사 등 복잡하지만 여기선 단순 계산
        est_price = int(base_price * (adj_rate / 100))
        
        # 6. 투찰률/낙찰률 (87.745% + 알파)
        # 운찰제 성격 반영
        bid_rate = 87.745 + np.random.exponential(0.05)
        winning_price = int(est_price * (bid_rate / 100))
        
        # 7. 데이터 추가 (실제 엑셀 컬럼명과 유사하게)
        data.append({
            '입찰공고번호': f"{2024000+i}-00",
            '입찰공고명': title,
            '공고기관명': agency_full,
            '개찰일시': dates[i].strftime('%Y-%m-%d %H:%M'),
            '기초금액': base_price,
            '예정가격': est_price,
            '낙찰금액': winning_price,
            '낙찰하한율': 87.745,
            '낙찰률': round(bid_rate, 4),
            # '사정율' 컬럼은 계산 가능하므로 일부러 뺄 수도 있지만, 사용 편의를 위해 포함 (옵션)
            '사정율': round(adj_rate, 5) 
        })

    df = pd.DataFrame(data)
    return df

if __name__ == "__main__":
    df = generate_realistic_data()
    # 엑셀 파일 생성
    filename = "2024_전기공사_개찰결과_샘플.xlsx"
    df.to_excel(filename, index=False)
    print(f"Created {filename}")
