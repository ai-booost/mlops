from abc import ABC, abstractmethod
from pathlib import Path
import pandas as pd
from icecream import ic

# Abstract FeatureStore class
class FeatureStore(ABC):
    """
    Feature Store의 추상 클래스입니다.
    """
    @abstractmethod
    def ingest_data(self, source_data: pd.DataFrame, feature_table: str):
        """
        데이터를 피처 저장소에 수집하는 메서드
        :param source_data: DataFrame 포함 features.
        :param feature_table: 데이터를 저장할 특징 테이블의 이름입니다.
        """
        pass

    @abstractmethod
    def retrieve_data(self, feature_table: str) -> pd.DataFrame:
        """
        피처 테이블에서 데이터를 검색하는 메서드
        :param feature_table: 검색할 기능 테이블의 이름입니다
        :return: DataFrame feature data.
        """
        pass

# LocalFeatureStore class that implements FeatureStore
class LocalFeatureStore(FeatureStore):
    """
    로컬 파일 시스템을 사용하여 Feature Store 구현.
    """
    def __init__(self, registry_path: str = "feature_store_registry"):
        """
        로컬 레지스트리 구조로 Feature Store를 초기화합니다
        :param registry_path: 레지스트리 디렉토리로의 경로.
        """
        self.registry_path = Path(registry_path)
        self.registry_path.mkdir(parents=True, exist_ok=True)
        ic(f"Feature store initialized at: {self.registry_path}")

    def ingest_data(self, source_data: pd.DataFrame, feature_table: str):
        """
        특징 저장소로 데이터를 수집합니다.
        :param source_data: DataFrame 포함 features.
        :param feature_table: 데이터를 저장할 특징 테이블의 이름입니다.
        """
        table_path = self.registry_path / f"{feature_table}.csv"
        source_data.to_csv(table_path, index=False)
        ic(f"Data ingested into feature table: {feature_table}")

    def retrieve_data(self, feature_table: str) -> pd.DataFrame:
        """
        피처 스토어의 피처 테이블에서 데이터를 검색합니다
        :param feature_table: 검색할 기능 테이블의 이름입니다
        :return: DataFrame feature data.
        """
        table_path = self.registry_path / f"{feature_table}.csv"
        if table_path.exists():
            ic(f"Retrieving data from feature table: {feature_table}")
            return pd.read_csv(table_path)
        else:
            raise FileNotFoundError(f"Feature table {feature_table} does not exist in the registry.")
