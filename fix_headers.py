import pandas as pd
import os

def fix_headers():
    file_path = '2024_전기공사_통합데이터.xlsx'
    
    if not os.path.exists(file_path):
        print("파일이 없습니다.")
        return

    df = pd.read_excel(file_path)
    
    print("현재 컬럼명:", df.columns.tolist())
    
    # 10개의 컬럼이 있다고 가정 (순서대로)
    # ['공고명', '발주처', '공고일', '기초금액', '예정가격', '낙찰금액', '낙찰하한율', '낙찰률', '사정율', '비고']
    # 만약 컬럼 개수가 다르면 앞에서부터 매핑
    
    correct_columns = ['공고명', '발주처', '공고일', '기초금액', '예정가격', '낙찰금액', '낙찰하한율', '낙찰률', '사정율', '비고']
    
    if len(df.columns) == len(correct_columns):
        df.columns = correct_columns
        print("컬럼명을 정상적으로 복구했습니다!")
    else:
        # 개수가 다르면, 혹시 '비고'가 없어서 9개일 수도 있음
        if len(df.columns) == 9:
            df.columns = ['공고명', '발주처', '공고일', '기초금액', '예정가격', '낙찰금액', '낙찰하한율', '낙찰률', '사정율']
            print("컬럼명을 복구했습니다 (비고 제외 9개)")
        else:
            print(f"⚠️ 컬럼 개수가 맞지 않아 자동 복구 실패 (현재 {len(df.columns)}개)")
            # 강제로 앞 8개라도 맞춤?
            # 일단 skip

    df.to_excel(file_path, index=False)
    print("파일을 다시 저장했습니다.")

if __name__ == "__main__":
    fix_headers()
