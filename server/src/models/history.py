from beanie import Document
from datetime import datetime
from typing import Any, Dict, List


class History(Document):
    user_id: str
    date: str = datetime.now().strftime("%d-%m-%Y")
    history_list: List[Dict[str, Any]] = []

    class Settings:
        name = "history"
