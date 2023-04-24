from models.file import File
from models.category import Category


async def get_files_info(user_id: str):
    files_info_dict = {
        "total_count": 0,
        "total_size": 0
    }

    async for file in File.find({
        "user_id": user_id,
    }):
        files_info_dict["total_count"] += 1
        files_info_dict["total_size"] += file.size

    return files_info_dict


async def get_custom_categories_info(user_id: str):
    category_info_dict = {
        "total_count": 0,
        "total_size": 0
    }

    async for category in Category.find({
        "user_id": user_id,
    }):
        if category.name == "default_category":
            continue

        category_info_dict["total_count"] += 1
        category_info_dict["total_size"] += category.size

    return category_info_dict


async def get_files_info_by_category(category_name: str, user_id: str):
    category_info_dict = {
        "total_count": 0,
        "total_size": 0
    }

    async for file in File.find({
        "user_id": user_id,
        "category_name": category_name,
        "metadata.is_basket": False,
        "metadata.is_favorite": False
    }):
        category_info_dict["total_count"] += 1
        category_info_dict["total_size"] += file.size

    return category_info_dict
