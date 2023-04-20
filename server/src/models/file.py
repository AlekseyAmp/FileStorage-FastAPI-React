from typing import Any, Dict, Optional
from beanie import Document


class File(Document):
    user_id: str
    name: str
    size: float
    content_type: str
    category_name: Optional[str]
    path: str
    metadata: Dict[str, Any] = {}

    class Settings:
        name = "files"
