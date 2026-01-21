import pandas as pd
import os

def check_duplicates():
    file_path = '2024_전기공사_통합데이터.xlsx'
    
    if not os.path.exists(file_path):
        print("파일이 없습니다.")
        return

    df = pd.read_excel(file_path)
    
    # 중복 기준: 공고명 + 발주처 (날짜는 조금 다를 수도 있으니 확실한 2개로 비교)
    duplicates = df[df.duplicated(subset=['공고명', '발주처'], keep=False)]
    
    if len(duplicates) > 0:
        print(f"⚠️ 총 {len(duplicates)}건의 중복 의심 데이터가 발견되었습니다!")
        print(duplicates[['공고명', '발주처', '공고일']].sort_values('공고명'))
        
        # 중복 제거 (첫 번째 것만 남김)
        df_clean = df.drop_duplicates(subset=['공고명', '발주처'], keep='first')
        print(f"\n✨ 중복을 제거하면 {len(df)}건 -> {len(df_clean)}건이 됩니다.")
        
        # 저장할까요?
        # df_clean.to_excel(file_path, index=False)
        return True
    else:
        print("No duplicate data found. It is clean!")
        return False

if __name__ == "__main__":
    check_duplicates()
