from datetime import datetime
from typing import Any, Dict, List
from beanie import Document


class FileHistory(Document):
    user_id: str
    date: str = datetime.now().strftime("%d-%m-%Y")
    time: str = datetime.now().strftime("%H:%M:%S")
    history_list_today: List[Dict[str, Any]] = []

    class Settings:
        name = "files_history"


class UserHistory(Document):
    user_id: str
    date: str = datetime.now().strftime("%d-%m-%Y")
    time: str = datetime.now().strftime("%H:%M:%S")
    history_list_today: List[Dict[str, Any]] = []

    class Settings:
        name = "users_history"