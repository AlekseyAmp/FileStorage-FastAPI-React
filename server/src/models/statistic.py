from beanie import Document
from pydantic import Field
from datetime import datetime


class TodayStatistic(Document):
    user_id: str
    date: str = datetime.now().strftime("%d-%m-%Y")
    actions: dict


    class Settings:
        name = "today_statistic"
