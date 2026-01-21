import pandas as pd
import os

def add_data():
    file_path = '2024_전기공사_통합데이터.xlsx'
    
    if not os.path.exists(file_path):
        print("파일이 없습니다.")
        return

    df = pd.read_excel(file_path)
    
    # 4차 배치 (3건) - 2026/01/21 추가 요청
    new_items = [
        {
            # Image 0: 당진중학교 외 2교 전기차충전시설 설치 전기공사
            # 투찰금액: 26,656,255, 투찰률: 90.281%
            # 공사예정금액: 29,592,000
            '공고명': '당진중학교 외 2교 전기차충전시설 설치 전기공사',
            '발주처': '충청남도당진교육지원청',
            '공고일': '2026-01-16',
            '낙찰금액': 26656255,
            '낙찰률': 90.281,
            '기초금액_화면': 29592000, 
            '비고': '정상'
        },
        {
            # Image 1: 구미교육지원청 청사 남측 부출입구 신설 전기공사
            # 투찰금액: 53,747,182, 투찰률: 90.061%
            # 공사예정금액: 59,631,000
            '공고명': '구미교육지원청 청사 남측 부출입구 신설 전기공사',
            '발주처': '경상북도구미교육지원청',
            '공고일': '2026-01-16',
            '낙찰금액': 53747182,
            '낙찰률': 90.061,
            '기초금액_화면': 59631000,
            '비고': '정상'
        },
        {
            # Image 2: 여좌천 일원 보행등 보수 전기공사
            # 투찰금액: 77,525,910, 투찰률: 90.231%
            # 공사예정금액: 90,264,000
            # 역산 예정가격: 77,525,910 / 0.90231 = 85,919,373
            # 차이: 약 430만원 (5% 이내) -> 정상 범위로 간주하고 화면상 금액을 기초금액으로 사용
            '공고명': '여좌천 일원 보행등 보수 전기공사',
            '발주처': '경상남도 창원시 진해구',
            '공고일': '2026-01-15',
            '낙찰금액': 77525910,
            '낙찰률': 90.231,
            '기초금액_화면': 90264000,
            '비고': '정상'
        }
    ]
    
    rows_to_add = []
    
    for item in new_items:
        # 1. 예정가격 역산
        est_price = int(item['낙찰금액'] / (item['낙찰률'] / 100))
        
        # 2. 기초금액 결정
        # 화면상 금액과 역산(예가)의 차이가 10% 이내면 정상, 기초금액_화면 사용
        if item['기초금액_화면'] > 0:
            diff_ratio = abs(item['기초금액_화면'] - est_price) / est_price
        else:
            diff_ratio = 999
            
        if diff_ratio < 0.1: # 10% 이내 차이는 정상 (자재비 등 미미하거나 없다고 판단)
            base_price = item['기초금액_화면']
            adj_rate = (est_price / base_price) * 100
            final_note = "정상"
        else:
            # 차이가 크면 보정
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
