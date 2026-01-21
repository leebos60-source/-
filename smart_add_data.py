import pandas as pd
import os

def smart_add_data(new_items):
    file_path = '2024_전기공사_통합데이터.xlsx'
    
    # 1. 파일 로드
    if os.path.exists(file_path):
        df = pd.read_excel(file_path)
    else:
        df = pd.DataFrame(columns=['공고명', '발주처', '공고일', '기초금액', '예정가격', '낙찰금액', '낙찰하한율', '낙찰률', '사정율'])
    
    rows_to_add = []
    skipped_count = 0
    
    for item in new_items:
        # 2. 중복 체크 (공고명 & 발주처가 같으면 이미 있는 것으로 간주)
        is_duplicate = not df[
            (df['공고명'] == item['공고명']) & 
            (df['발주처'] == item['발주처'])
        ].empty
        
        if is_duplicate:
            print(f"[SKIP] 이미 존재하는 데이터입니다: {item['공고명']}")
            skipped_count += 1
            continue
            
        # 3. 데이터 계산 및 준비
        
        # 3-1. 예정가격 역산
        est_price = int(item['낙찰금액'] / (item['낙찰률'] / 100))
        
        # 3-2. 기초금액 결정 (화면값 vs 역산값 비교)
        if '기초금액_화면' in item and item['기초금액_화면'] > 0:
            diff_ratio = abs(item['기초금액_화면'] - est_price) / est_price
            if diff_ratio < 0.1: 
                base_price = item['기초금액_화면']
                adj_rate = (est_price / base_price) * 100
                final_note = "정상"
            else:
                base_price = est_price 
                adj_rate = 100.0
                final_note = "보정됨"
        else:
             # 기초금액 정보가 아예 없으면 역산값 사용
            base_price = est_price
            adj_rate = 100.0
            final_note = "기초금액미상_대체"

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
        print(f"[ADD] 추가됩니다: {item['공고명']} (사정율 {adj_rate:.2f}%)")

    # 4. 저장
    if rows_to_add:
        new_df = pd.DataFrame(rows_to_add)
        merged_df = pd.concat([df, new_df], ignore_index=True)
        merged_df.to_excel(file_path, index=False)
        print(f"\n✨ {len(rows_to_add)}건 추가 완료! (총 {len(merged_df)}건)")
    else:
        print("\n💤 추가된 데이터가 없습니다. (모두 중복이거나 빈 데이터)")

    return len(rows_to_add)
