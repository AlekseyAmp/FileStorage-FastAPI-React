from utils.file_utils import is_allowed_format
from models.file import File


async def get_files_by_category(category: str, user_id: str):
    files = []
    async for file in File.find():
        if file.user_id == user_id and is_allowed_format(file.name.split('.')[1], category):
            files.append(file)        
    return files

