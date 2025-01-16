from datetime import datetime, timedelta

from dateutil.relativedelta import relativedelta

class WeatherRequests:
    def __init__(self, start_time: datetime, end_time: datetime, location_id: str = 108):
        self.start_time = start_time
        self.end_time = end_time
        self.location_id = location_id
        self.help = 0

    @staticmethod
    def create_month_range(start_time: datetime, month_range: int):
        end_time = start_time + relativedelta(months=month_range)
        return WeatherRequests(start_time, end_time)
