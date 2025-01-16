from io import StringIO

import pandas as pd
import requests
from src.dataset.weather_requests import WeatherRequests
from src.dataset.weather_datasource import WeatherDataSource


class KmaApiClient(WeatherDataSource):
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
        print(params)

        response = requests.get(self.BASE_URL, params=params)
        if response.status_code == 200:
            return self.parse_to_dataframe(response.text, translate_to_korean=True)
        else:
            response.raise_for_status()

    def fetch_monthly_range_data(self, request: WeatherRequests) -> pd.DataFrame:
        data_frames = []
        date_offset = pd.DateOffset(months=1)
        current_time = request.start_time

        while current_time < request.end_time:
            next_time = current_time + date_offset
            response = self.fetch_data(
                current_time.strftime("%Y%m%d%H%M"),
                (next_time - pd.DateOffset(days=1)).replace(hour=23, minute=59).strftime("%Y%m%d%H%M"),
                request.location_id
            )
            print(response.head(1))
            print(response.tail(1))
            data_frames.append(response)
            current_time = next_time

        return pd.concat(data_frames)

    def parse_to_dataframe(self, raw_data, translate_to_korean=False):
        lines = raw_data.strip().split("\n")
        data_lines = [line for line in lines if not line.startswith("#")]

        # Define column names as per the header provided with more descriptive names
        columns = [
            "ObservationTime", "StationID", "WindDirection", "WindSpeed", "GustDirection", "GustSpeed", "GustTime",
            "LocalPressure", "SeaLevelPressure", "PressureTrend",
            "PressureChange", "Temperature", "DewPointTemperature", "RelativeHumidity", "VaporPressure",
            "HourlyRainfall", "DailyRainfall", "CumulativeRainfall", "RainfallIntensity", "SnowDepth3Hr",
            "DailySnowDepth", "TotalSnowDepth", "CurrentWeatherCode", "PastWeatherCode", "WeatherCode",
            "TotalCloudCover", "MidLowCloudCover", "LowestCloudHeight", "CloudType", "UpperCloudType",
            "MidCloudType", "LowCloudType", "Visibility", "SunshineDuration", "SolarRadiation", "GroundCondition",
            "GroundTemperature", "SoilTemperature5cm", "SoilTemperature10cm", "SoilTemperature20cm",
            "SoilTemperature30cm",
            "SeaCondition", "WaveHeight", "MaxWindForce", "PrecipitationData", "ObservationType"
        ]

        if translate_to_korean:
            korean_columns = [
                "관측시각", "지점번호", "풍향", "풍속", "돌풍방향", "돌풍속도", "돌풍시각", "현지기압", "해면기압", "기압경향",
                "기압변화량", "기온", "이슬점온도", "상대습도", "수증기압", "시간강수량", "일강수량", "누적강수량", "강수강도", "3시간적설",
                "일적설", "총적설", "현재날씨코드", "과거날씨코드", "일기코드", "전운량", "중하층운량", "최저운고", "운형", "상층운형",
                "중층운형", "하층운형", "시정", "일조시간", "일사량", "지면상태", "지면온도", "5cm지중온도", "10cm지중온도", "20cm지중온도", "30cm지중온도",
                "해면상태", "파고", "최대풍력", "강수자료", "관측유형"
            ]
            columns = korean_columns

        # Use pandas to parse the dataset into a DataFrame
        return pd.read_csv(StringIO("\n".join(data_lines)), delim_whitespace=True, header=None, names=columns)
