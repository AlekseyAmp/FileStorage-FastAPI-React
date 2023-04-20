from typing import Any, Dict, Optional
from beanie import Document


class Category(Document):
    user_id: str
    name: str
    size: float
    path: str
    metadata: Dict[str, Any] = {}

    class Settings:
        name = "categories"
