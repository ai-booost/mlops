import sys
from pathlib import Path

project_root = Path(__file__).resolve().parents[3]  # collect.py에서 3단계 상위 디렉토리
sys.path.append(str(project_root))

import pandas as pd

from src.features.registry.data_pipeline import DataPipeline
from src.features.registry.feature_store import FeatureStore, LocalFeatureStore

dotenv_path = project_root / ".env"
root_data_dir = project_root / "data"
file_name_all = "weather_all.csv"
file_name_monthly = "weather_monthly.csv"
file_name_daily = "weather_daily.csv"


# 피처 레지스트리
class FeatureRegistry:
    """
    피처 레지스트리 클래스.
    command: [python feature_registry.py load_all_data, python feature_registry.py load_daily_data]
    """
    # registry_dir = project_root / 'feature_store_registry'
    registry_dir = Path(root_data_dir / 'feature_store_registry')

    def __init__(self, feature_store: FeatureStore = LocalFeatureStore(registry_dir)):
        self.feature_store: FeatureStore = feature_store
        self.data_pipeline = DataPipeline(self.feature_store)
        self.feature_store_name = "feature_store_registry"

    def batch_all_data(self):
        """
        데이터를 준비하는 함수.
        """
        # 데이터 불러오기
        source_data = pd.read_csv(root_data_dir / file_name_all)

        # 파이프라인 실행
        processed_data = self.data_pipeline.run_pipeline(source_data)

        self.feature_store.save_data(processed_data, self.feature_store_name)

    def batch_daily_data(self):
        """
        데이터를 준비하는 함수.
        """
        # 데이터 불러오기
        source_data = pd.read_csv(root_data_dir / file_name_daily)

        # 파이프라인 실행
        processed_data = self.data_pipeline.run_pipeline(source_data)

        self.feature_store.save_data(processed_data, self.feature_store_name)
