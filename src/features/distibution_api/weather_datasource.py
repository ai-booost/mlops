"""
날씨 데이터를 가져오는 데이터 소스 인터페이스를 정의한 파일
"""
from abc import ABC, abstractmethod
from datetime import datetime

import pandas as pd

from src.features.distibution_api.weather_requests import WeatherRequests

# 데이터 소스 인터페이스 정의
class WeatherDataSource(ABC):
    """
    날씨 데이터를 가져오는 데이터 소스 인터페이스
    """

    @abstractmethod
    def fetch_data(self, start_time: datetime, end_time: datetime, station_id: str) -> pd.DataFrame:
        """데이터를 가져오는 메서드"""

    @abstractmethod
    def fetch_monthly_range_data(self, request: WeatherRequests) -> pd.DataFrame:
        """기간을 지정하여 데이터를 가져오는 메서드"""

    @abstractmethod
    def fetch_daily_range_data(self, request_params: WeatherRequests) -> pd.DataFrame:
        """일일 데이터를 가져오는 메서드"""

class KmaApiClient(WeatherDataSource):
    """
    기상청 API 클라이언트 클래스.

    Attributes:
        BASE_URL (str): The base URL for the KMA API.
    """
    BASE_URL = "https://apihub.kma.go.kr/api/typ01/url/kma_sfctm3.php"

    def __init__(self, auth_key):
        self.auth_key = auth_key

    def fetch_data(self, start_time: str, end_time: str, station_id: str) -> pd.DataFrame:
        params = {
            "tm1": start_time,
            "tm2": end_time,
            "stn": station_id,
            "authKey": self.auth_key,
            "help": 0
        }

        try:
            response = requests.get(self.BASE_URL, params=params, timeout=60)
            response.raise_for_status()  # 상태 코드가 4xx 또는 5xx이면 예외 발생
            return self.parse_to_dataframe(response.text, translate_to_korean=True)
        except requests.exceptions.Timeout as e:
            raise RuntimeError("Request to KMA API timed out.") from e
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"Failed to fetch data from KMA API: {e}") from e

    def fetch_monthly_range_data(self, request: WeatherRequests) -> pd.DataFrame:
        data_frames = []
        date_offset = pd.DateOffset(months=1)
        current_time = request.start_time

        while current_time < request.end_time:
            next_time = current_time + date_offset
            next_time_param = ((next_time - pd.DateOffset(days=1))
                               .replace(hour=23, minute=59).strftime("%Y%m%d%H%M"))
            response = self.fetch_data(
                current_time.strftime("%Y%m%d%H%M"),
                next_time_param,
                request.location_id
            )
            data_frames.append(response)
            current_time = next_time

        return pd.concat(data_frames)

    def fetch_daily_range_data(self, request_params: WeatherRequests):
        return self.fetch_data(
            request_params.start_time.strftime("%Y%m%d%H%M"),
            request_params.end_time.strftime("%Y%m%d%H%M"),
            request_params.location_id
        )

    def parse_to_dataframe(self, raw_data, translate_to_korean=False):
        """
        Parse the raw data into a DataFrame.
        :param raw_data:
        :param translate_to_korean:
        :return:
        """
        lines = raw_data.strip().split("\n")
        data_lines = [line for line in lines if not line.startswith("#")]

        # Define column names as per the header provided with more descriptive names
        columns = [
            "ObservationTime", "StationID", "WindDirection",
            "WindSpeed", "GustDirection", "GustSpeed", "GustTime",
            "LocalPressure", "SeaLevelPressure", "PressureTrend",
            "PressureChange", "Temperature", "DewPointTemperature",
            "RelativeHumidity", "VaporPressure",
            "HourlyRainfall", "DailyRainfall", "CumulativeRainfall",
            "RainfallIntensity", "SnowDepth3Hr",
            "DailySnowDepth", "TotalSnowDepth", "CurrentWeatherCode",
            "PastWeatherCode", "WeatherCode",
            "TotalCloudCover", "MidLowCloudCover", "LowestCloudHeight",
            "CloudType", "UpperCloudType",
            "MidCloudType", "LowCloudType", "Visibility", "SunshineDuration",
            "SolarRadiation", "GroundCondition",
            "GroundTemperature", "SoilTemperature5cm",
            "SoilTemperature10cm", "SoilTemperature20cm",
            "SoilTemperature30cm",
            "SeaCondition", "WaveHeight", "MaxWindForce",
            "PrecipitationData", "ObservationType"
        ]

        if translate_to_korean:
            korean_columns = [
                "관측시각", "지점번호", "풍향",
                "풍속", "돌풍방향", "돌풍속도",
                "돌풍시각", "현지기압", "해면기압", "기압경향",
                "기압변화량", "기온", "이슬점온도",
                "상대습도", "수증기압", "시간강수량",
                "일강수량", "누적강수량", "강수강도", "3시간적설",
                "일적설", "총적설", "현재날씨코드",
                "과거날씨코드", "일기코드", "전운량",
                "중하층운량", "최저운고", "운형", "상층운형",
                "중층운형", "하층운형", "시정", "일조시간",
                "일사량", "지면상태", "지면온도",
                "5cm지중온도", "10cm지중온도", "20cm지중온도", "30cm지중온도",
                "해면상태", "파고", "최대풍력", "강수자료", "관측유형"
            ]
            columns = korean_columns

        # Use pandas to parse the dataset into a DataFrame
        return pd.read_csv(StringIO("\n".join(data_lines)),
                           delim_whitespace=True,
                           header=None,
                           names=columns)

