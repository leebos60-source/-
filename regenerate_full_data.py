import os
import pandas as pd
import importlib.util

# 스크립트 실행 순서
scripts = [
    'create_merged_data.py',    # 기본 100건 + 초기 3건
    'add_image_data.py',        # 1차 추가
    'add_more_images.py',       # 2차 추가
    'add_more_images_2.py',     # 3차 추가
    'add_more_images_3.py',     # 4차 추가
    'add_more_images_4.py',     # 5차 추가
    'add_more_images_5.py',     # 6차 추가
]

def run_script(script_name):
    print(f"run_script: {script_name}...")
    try:
        # 파일 경로
        script_path = os.path.abspath(script_name)
        
        # 모듈 로드 및 실행
        spec = importlib.util.spec_from_file_location("__main__", script_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        print(f"[Done] {script_name}")
    except Exception as e:
        print(f"[Fail] {script_name}: {e}")

def main():
    target_file = '2024_전기공사_통합데이터.xlsx'
    
    # 1. 기존 파일 삭제 (완전 초기화)
    if os.path.exists(target_file):
        try:
            os.remove(target_file)
            print(f"Deleted existing file: {target_file}")
        except Exception as e:
            print(f"Failed to delete file: {e}")
            return

    # 2. 순서대로 실행
    print("Starting full data regeneration...")
    for script in scripts:
        run_script(script)
        
    # 3. 결과 검증
    if os.path.exists(target_file):
        df = pd.read_excel(target_file)
        print(f"\n[SUCCESS] Final data file created!")
        print(f"Total rows: {len(df)}")
        print(f"Columns: {df.columns.tolist()}")
        
        # 중요 컬럼 확인
        if '낙찰률' in df.columns:
             print("[OK] '낙찰률' column exists.")
        else:
             print("[WARNING] '낙찰률' columnMISSING!")
    else:
        print("[ERROR] File not created.")

if __name__ == "__main__":
    main()
