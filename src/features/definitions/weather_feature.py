import pandas as pd


class WeatherFeature:
    """
       날씨 관련 피처 생성 클래스
       - 온도, 강수량, 습도 관련 피처 정의
   """

    @staticmethod
    def create_features(weather_data: pd.DataFrame) -> pd.DataFrame:
        """
        날씨 데이터로부터 주요 피처 생성
        Args:
            weather_data (pd.DataFrame): 원본 날씨 데이터
                - 컬럼 예시: ['date', 'temperature', 'precipitation', 'humidity']
        Returns:
            pd.DataFrame: 피처가 추가된 데이터프레임
        """
        # 기본 피처 추가
        weather_data['temp_diff'] = weather_data['temperature'].diff()  # 온도 변화량
        weather_data['precip_flag'] = (weather_data['precipitation'] > 0).astype(int)  # 강수 여부 (0: 없음, 1: 있음)
        weather_data['humidity_diff'] = weather_data['humidity'].diff()  # 습도 변화량

        # 파생 피처 추가
        weather_data['temp_avg_7d'] = weather_data['temperature'].rolling(window=7).mean()  # 7일 평균 온도
        weather_data['precip_sum_7d'] = weather_data['precipitation'].rolling(window=7).sum()  # 7일 강수량 합계
        weather_data['humidity_avg_7d'] = weather_data['humidity'].rolling(window=7).mean()  # 7일 평균 습도

        return weather_data
