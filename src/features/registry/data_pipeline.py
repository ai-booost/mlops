from datetime import datetime

import pandas as pd
from icecream import ic

from src.features.registry.feature_store import FeatureStore

# 데이터 파이프라인 클래스
class DataPipeline:
    def __init__(self, feature_store: FeatureStore):
        """
        피처 스토어를 참조하여 데이터 파이프라인을 초기화합니다.
        :param feature_store: FeatureStore 클래스의 인스턴스
        """
        self.feature_store = feature_store

    def run_pipeline(self, source_data: pd.DataFrame, feature_table: str):
        """
        데이터 파이프라인을 실행하여 데이터를 처리하고 피처 스토어에 저장합니다.
        :param source_data: DataFrame containing raw input data.
        :param feature_table: Name of the feature table to store processed data.
        """
        ic("Starting data pipeline...")
        processed_data = self.process_data(source_data)
        processed_data = processed_data[['관측시각','시간강수량', '일강수량', '누적강수량','풍향','풍속','기온','일적설','총적설','상대습도','기압변화량']]

        # 음수를 0으로 대체할 컬럼 목록
        columns_to_replace = ['시간강수량', '일강수량', '누적강수량', '풍속', '풍향', '일적설', '총적설', '상대습도']

        # 음수를 0으로 대체
        processed_data[columns_to_replace] = processed_data[columns_to_replace].clip(lower=0)

        self.feature_store.ingest_data(processed_data, feature_table)
        ic("Data pipeline completed.")

    def process_data(self, source_data: pd.DataFrame) -> pd.DataFrame:
        """
        원시 입력 데이터(예: 데이터 정리, 기능 엔지니어링)를 처리합니다.
        :param source_data: Raw input data.
        :return: Processed DataFrame.
        """
        ic("Processing data...")
        # Example processing step: Add a processed timestamp
        source_data["processed_timestamp"] = datetime.now()
        return source_data