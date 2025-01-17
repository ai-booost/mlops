import os
import sys
from pathlib import Path

project_root = Path(__file__).resolve().parents[3]
sys.path.append(str(project_root))

from pathlib import Path
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv
from icecream import ic
import fire

from src.features.distibution_api.weather_datasource import KmaApiClient
from src.features.distibution_api.weather_requests import WeatherRequests

dotenv_path = project_root / ".env"
root_data_dir = project_root / "data"
file_name_all = "weather_all.csv"
file_name_monthly = "weather_monthly.csv"
file_name_daily = "weather_daily.csv"


def load_api_key():
    load_dotenv(dotenv_path)
    auth_key = os.environ.get("KMA_API_KEY")
    if not auth_key:
        raise ValueError("KMA_API_KEY가 설정되지 않았습니다.")
    return auth_key


def save(output_file_name: str, response: pd.DataFrame):
    dir_path = os.path.dirname(output_file_name)
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    response.to_csv(output_file_name, index=False)


class WeatherDataProcessor:
    def __init__(self, output_path=root_data_dir):
        self.output_path = output_path
        self.auth_key = load_api_key()
        self.weather_data_source = KmaApiClient(self.auth_key)

    def run_data_prepare_month(self, start_year, start_month, month_range_count=1,
                               output_file_name: str = file_name_all):
        output_file = os.path.join(self.output_path, output_file_name)
        start_time = datetime(start_year, start_month, 1)
        request_params = WeatherRequests.create_month_range(start_time, month_range_count)

        response = self.weather_data_source.fetch_monthly_range_data(request_params)

        save(output_file, response)
        ic(f"데이터가 {output_file}에 저장되었습니다.")

    def run_data_prepare_day(self, year, month, day, output_file_name=file_name_daily):
        output_file = os.path.join(self.output_path, output_file_name)
        start_time = datetime(year, month, day)
        request_params = WeatherRequests.create_day_range(start_time)

        response = self.weather_data_source.fetch_daily_range_data(request_params)

        save(output_file, response)
        ic(f"데이터가 {output_file}에 저장되었습니다.")

    def run_data_prepare_all(self, start_year:str, output_file_name=file_name_all):
        """
        start_year부터 현재까지의 데이터를 모두 가져옵니다.
        :param output_file_name:
        :param start_year:
        :return:
        """
        current_date = datetime.now()
        current_year = current_date.year
        current_month = current_date.month

        start_year = int(start_year)

        if start_year == current_year:
            month_range_count = current_month - 1
        else:
            month_range_count = (current_year - start_year - 1) * 12 + 12 + current_month

        self.run_data_prepare_month(start_year, 1, month_range_count, output_file_name)

    def run_data_prepare_current_month(self):
        """
        현재 월의 데이터를 가져옵니다.
        :return:
        """
        self.run_data_prepare_month(datetime.now().year, datetime.now().month, 1, file_name_monthly)

    def run_data_prepare_today(self):
        """
        오늘의 데이터를 가져옵니다.
        :return:
        """
        self.run_data_prepare_day(datetime.now().year, datetime.now().month, datetime.now().day, file_name_daily)



def runner():
    """
    Command line interface for weather data processing.
    python weather_client.py run_data_prepare_month_range --start_year=2010
    python weather_client.py run_data_prepare_current_month
    python weather_client.py run_data_prepare_today
    """
    processor = WeatherDataProcessor()

    fire.Fire({
        "run_data_prepare_month_range": processor.run_data_prepare_month,
        "run_data_prepare_today": processor.run_data_prepare_today,
        "run_data_prepare_current_month": processor.run_data_prepare_current_month,
        "run_data_prepare_all": processor.run_data_prepare_all
    })


if __name__ == "__main__":
    runner()
