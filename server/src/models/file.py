from typing import Any, Dict
from beanie import Document

class File(Document):
    
    user_id: str
    name: str
    content_type: str
    path: str
    size: float
    metadata: Dict[str, Any] = {}

    class Settings:
        name = "files"
