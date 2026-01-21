import pandas as pd
import os

def add_data():
    file_path = '2024_전기공사_통합데이터.xlsx'
    
    if not os.path.exists(file_path):
        print("파일이 없습니다.")
        return

    df = pd.read_excel(file_path)
    
    # 5차 배치 (4건) - 2026/01/21 추가 요청
    new_items = [
        {
            # Image 0: 군서초 후관동 화장실개조 및 급식실동 창고 증축 전기공사
            # 투찰금액: 31,736,657, 투찰률: 90.222%
            # 공사예정금액: 35,207,000
            # 역산: 35,176,184 (차이 미미, 정상)
            '공고명': '군서초 후관동 화장실개조 및 급식실동 창고 증축 전기공사',
            '발주처': '전라남도영광교육지원청',
            '공고일': '2026-01-16',
            '낙찰금액': 31736657,
            '낙찰률': 90.222,
            '기초금액_화면': 35207000, 
            '비고': '정상'
        },
        {
            # Image 1: 순천부영초 외 4교 내진보강 외 3건 전기공사
            # 투찰금액: 44,459,700, 투찰률: 90.289%
            # 공사예정금액: 48,978,000
            '공고명': '순천부영초 외 4교 내진보강 외 3건 전기공사',
            '발주처': '전라남도순천교육지원청',
            '공고일': '2026-01-16',
            '낙찰금액': 44459700,
            '낙찰률': 90.289,
            '기초금액_화면': 48978000,
            '비고': '정상'
        },
        {
            # Image 2: 해양수련원 조리실 환기설비개선 전기공사
            # 투찰금액: 29,869,031, 투찰률: 90.319%
            # 공사예정금액: 33,114,000
            '공고명': '해양수련원 조리실 환기설비개선 전기공사',
            '발주처': '충청남도보령교육지원청',
            '공고일': '2026-01-15',
            '낙찰금액': 29869031,
            '낙찰률': 90.319,
            '기초금액_화면': 33114000,
            '비고': '정상'
        },
        {
            # Image 3: 광주자연과학고 노후 급식실 환경개선 전기공사 감리용역
            # 투찰금액: 13,290,290, 투찰률: 90.04%
            # 용역이므로 기초금액 화면 확인 어려움 -> 역산값 사용 및 사정율 100% 가정 (보수적 접근)
            '공고명': '광주자연과학고 노후 급식실 환경개선 전기공사 감리용역',
            '발주처': '광주광역시교육청',
            '공고일': '2026-01-15',
            '낙찰금액': 13290290,
            '낙찰률': 90.04,
            '기초금액_화면': 0, # 확인불가
            '비고': '감리용역_보정'
        }
    ]
    
    rows_to_add = []
    
    for item in new_items:
        # 1. 예정가격 역산
        est_price = int(item['낙찰금액'] / (item['낙찰률'] / 100))
        
        # 2. 기초금액 결정
        if item['기초금액_화면'] > 0:
            diff_ratio = abs(item['기초금액_화면'] - est_price) / est_price
        else:
            diff_ratio = 999
            
        if diff_ratio < 0.1: 
            base_price = item['기초금액_화면']
            adj_rate = (est_price / base_price) * 100
            final_note = "정상"
        else:
            base_price = est_price 
            adj_rate = 100.0
            final_note = f"{item['비고']}-보정됨"
            
        print(f"Added: {item['공고명']} | 사정율: {adj_rate:.2f}% ({final_note})")

        row = {
            '공고명': item['공고명'],
            '발주처': item['발주처'],
            '공고일': item['공고일'],
            '기초금액': base_price,
            '예정가격': est_price,
            '낙찰금액': item['낙찰금액'],
            '낙찰하한율': 87.745,
            '낙찰률': item['낙찰률'],
            '사정율': adj_rate
        }
        rows_to_add.append(row)
    
    new_df = pd.DataFrame(rows_to_add)
    merged_df = pd.concat([df, new_df], ignore_index=True)
    
    merged_df.to_excel(file_path, index=False)
    print(f"Total rows: {len(merged_df)}")

if __name__ == "__main__":
    add_data()
