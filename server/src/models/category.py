from typing import Any, Dict
from beanie import Document


class Category(Document):
    user_id: str
    name: str
    name_for_search: str
    size: float
    path: str
    metadata: Dict[str, Any] = {}

    class Settings:
        name = "categories"
