import pandas as pd
import numpy as np

class Analyzer:
    def __init__(self):
        pass

    def analyze_adjustment_rates(self, df):
        """
        사정율 데이터의 기술 통계량을 반환합니다.
        """
        stats = df['사정율'].describe()
        return stats

    def calculate_winning_probability_ranges(self, df, base_price, limit_rate=87.745):
        """
        과거 사정율 분포를 기반으로, 어떤 사정율 구간이 가장 빈도가 높았는지 분석하여
        추천 투찰 금액을 계산합니다.
        
        limit_rate: 낙찰하한율 (예: 87.745, 86.745 등)
        """
        # 사정율 구간을 0.2% 단위로 나눕니다.
        bins = np.arange(97.0, 103.0, 0.2)
        counts, bin_edges = np.histogram(df['사정율'], bins=bins)
        
        # 가장 빈도가 높은 구간 Top 3
        top_indices = counts.argsort()[-3:][::-1] # 내림차순 정렬
        
        recommendations = []
        for idx in top_indices:
            start_range = bin_edges[idx]
            end_range = bin_edges[idx+1]
            center_rate = (start_range + end_range) / 2
            
            # 추천 사정율
            rec_adj_rate = center_rate
            
            # 예상 예정가격
            est_price = base_price * (rec_adj_rate / 100)
            
            # 추천 투찰금액 (낙찰하한율 + 안전마진 0.005%p for safety rounding)
            # 보통 소수점 처리를 위해 아주 살짝 높게 씁니다.
            target_rate = limit_rate + 0.005
            bid_price = int(est_price * (target_rate / 100))
            
            recommendations.append({
                'label': f"다빈도 구간 {idx+1}위 ({start_range:.1f}% ~ {end_range:.1f}%)",
                'adj_rate': rec_adj_rate,
                'bid_price': bid_price,
                'count': counts[idx]
            })
            
        return recommendations
