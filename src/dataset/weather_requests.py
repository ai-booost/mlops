"""
기상청 요청 파라미터
"""
from datetime import datetime

from dateutil.relativedelta import relativedelta

class WeatherRequests:
    """
    기상청 요청 파라미터
    """
    # pylint: disable=R0903
    def __init__(self, start_time: datetime, end_time: datetime, location_id: str = 108):
        self.start_time = start_time
        self.end_time = end_time
        self.location_id = location_id
        self.help = 0

    @staticmethod
    def create_month_range(start_time: datetime, month_range: int):
        """
        Create a WeatherRequests object with a month range.
        :param start_time:
        :param month_range:
        :return:
        """
        end_time = start_time + relativedelta(months=month_range)
        return WeatherRequests(start_time, end_time)
