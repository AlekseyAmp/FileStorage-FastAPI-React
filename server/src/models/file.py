from typing import Any, Dict
from beanie import Document


class File(Document):
    user_id: str
    name: str
    size: float
    content_type: str
    category_name: str
    path: str
    metadata: Dict[str, Any] = {}

    class Settings:
        name = "files"
