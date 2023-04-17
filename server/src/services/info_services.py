from utils.file_utils import is_allowed_format
from models.file import File


async def get_files_info(user_id: str):
    files_info = {
        "total_count": 0,
        "total_size": 0
    }

    files = await File.find({
        "user_id": user_id
    }).to_list()

    if files:
        files_info["total_count"] = len(files)
        files_info["total_size"] = sum(file.size for file in files)

    return files_info


async def get_files_info_by_category(category: str, user_id: str):
    category_info = {
        "total_count": 0,
        "total_size": 0
    }

    async for file in File.find({
        "user_id": user_id
    }):
        if is_allowed_format(file.name.split('.')[1], category):
            category_info["total_count"] += 1
            category_info["total_size"] += file.size

    return category_info
