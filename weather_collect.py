"""
이 모듈은 기상청(KMA)의 날씨 데이터를 가져와 데이터 준비 과정을 자동화합니다.
사용자가 시작 연도, 시작 월, 가져올 개월 수, 출력 파일 경로를 입력하면 데이터를 처리하여 CSV 파일로 저장합니다.
"""
import os
import sys
from datetime import datetime

import fire
from dotenv import load_dotenv
from icecream import ic

from src.dataset.weather_requests import WeatherRequests
from src.dataset.weather_datasource import WeatherDataSource
from src.dataset.kma_client import KmaApiClient

sys.path.append(os.path.dirname(os.path.abspath(__file__)))


def run_data_prepare(start_year, start_month, month_range_count, output_file):
    """
    데이터를 준비하는 함수.
    :param start_year: 시작 연도
    :param start_month: 시작 월
    :param month_range_count: 가져올 개월 수
    :param output_file: 출력 파일 경로
    """
    load_dotenv()
    auth_key = os.environ.get("KMA_API_KEY")
    if not auth_key:
        raise ValueError("KMA_API_KEY가 설정되지 않았습니다.")

    weather_data_source: WeatherDataSource = KmaApiClient(auth_key)
    start_time = datetime(start_year, start_month, 1)
    request_params = WeatherRequests.create_month_range(start_time, month_range_count)
    response = weather_data_source.fetch_monthly_range_data(request_params)
    response.to_csv(output_file, index=False)
    ic(f"데이터가 {output_file}에 저장되었습니다.")


if __name__ == "__main__":
    fire.Fire({
        "run_data_prepare": run_data_prepare,
    })
