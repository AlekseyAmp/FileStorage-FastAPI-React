from typing import Any, Dict, List
from beanie import Document

from constants.history_constants import today_date


class FileHistory(Document):
    user_id: str
    date: str = today_date
    history_list: List[Dict[str, Any]] = []

    class Settings:
        name = "files_history"


class UserHistory(Document):
    user_id: str
    date: str = today_date
    history_list: List[Dict[str, Any]] = []

    class Settings:
        name = "users_history"
