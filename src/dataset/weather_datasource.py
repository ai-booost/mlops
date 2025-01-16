from abc import ABC, abstractmethod
from datetime import datetime

import pandas as pd

from src.dataset.weather_requests import WeatherRequests

# 1. 데이터 소스 인터페이스 정의
class WeatherDataSource(ABC):
    @abstractmethod
    def fetch_data(self, start_time: datetime, end_time: datetime, station_id: str) -> pd.DataFrame:
        """데이터를 가져오는 메서드"""
        pass

    @abstractmethod
    def fetch_monthly_range_data(self, request: WeatherRequests) -> pd.DataFrame:
        """기간을 지정하여 데이터를 가져오는 메서드"""
        pass
