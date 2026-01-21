import pandas as pd
import numpy as np

file_path = '2024_전기공사_통합데이터.xlsx'
df = pd.read_excel(file_path)

# Mock Data: Rows 3 to 102 (indices) -> iloc[3:103] actually, let's correspond to the text.
# Step 220 created 103 rows. First 3 real, next 100 mock.
# Indices 0,1,2 = Real
# Indices 3..102 = Mock (100 rows)
# Indices 103..end = Real (added manually)

mock_df = df.iloc[3:103]
real_df = pd.concat([df.iloc[0:3], df.iloc[103:]])

print(f"Mock Data Count: {len(mock_df)}")
print(f"Real Data Count: {len(real_df)}")

def print_stats(name, data):
    print(f"\n--- {name} Analysis ---")
    print(data[['사정율', '낙찰률']].describe())
    print(f"사정율 Variance: {data['사정율'].var():.4f}")

print_stats("Mock Data", mock_df)
print_stats("Real Data", real_df)

# Check distribution center
print("\n--- Key Differences ---")
print(f"Mock Mean Adj Rate: {mock_df['사정율'].mean():.4f}%")
print(f"Real Mean Adj Rate: {real_df['사정율'].mean():.4f}%")
