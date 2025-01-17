import sys
from pathlib import Path

project_root = Path(__file__).resolve().parents[3]  # collect.py에서 3단계 상위 디렉토리
sys.path.append(str(project_root))

import fire
import pandas as pd

from src.features.registry.data_pipeline import DataPipeline
from src.features.registry.feature_store import FeatureStore, LocalFeatureStore

dotenv_path = project_root / ".env"
root_data_dir = project_root / "data"
file_name_monthly = "weather_monthly.csv"
file_name_daily = "weather_daily.csv"


# 피처 레지스트리
class FeatureRegistry:
    """
    피처 레지스트리 클래스.
    command: [python feature_registry_client.py load_all_data, python feature_registry_client.py load_daily_data]
    """
    def __init__(self, feature_store: FeatureStore = LocalFeatureStore()):
        self.feature_store: FeatureStore = feature_store
        self.data_pipeline = DataPipeline(self.feature_store)
        self.feature_store_name = "feature_store_registry"

    def load_all_data(self):
        """
        데이터를 준비하는 함수.
        """
        # 데이터 불러오기
        source_data = pd.read_csv(root_data_dir / file_name_monthly)

        # 파이프라인 실행
        self.data_pipeline.run_pipeline(source_data, feature_table=self.feature_store_name)

        # Feature Store 저장
        self.feature_store.retrieve_data(self.feature_store_name)

    def load_daily_data(self):
        """
        데이터를 준비하는 함수.
        """
        # 데이터 불러오기
        source_data = pd.read_csv(root_data_dir / file_name_daily)

        # 파이프라인 실행
        self.data_pipeline.run_pipeline(source_data, feature_table=self.feature_store_name)

        # Feature Store 저장
        self.feature_store.retrieve_data(self.feature_store_name)

def runner():
    fire.Fire(FeatureRegistry(LocalFeatureStore()))

if __name__ == "__main__":
    runner()
