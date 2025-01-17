import pandas as pd
from datetime import datetime
from pathlib import Path

from icecream import ic

from src.features.registry.data_pipeline import DataPipeline
from src.features.registry.feature_store import FeatureStore


# Example usage
def main():
    # FeatureStore 인스턴스 생성
    feature_store = FeatureStore()

    # DataPipeline 인스턴스 생성
    data_pipeline = DataPipeline(feature_store)

    # 데이터 불러오기
    source_data = pd.read_csv("../../dataset/raw/kma_data_2010-2020.csv")

    # 파이프라인 실행
    data_pipeline.run_pipeline(source_data, feature_table="customer_features")

    # Feature Store 저장
    retrieved_data = feature_store.retrieve_data("customer_features")
    ic("Retrieved Data:")
    ic(retrieved_data)

if __name__ == "__main__":
    main()

