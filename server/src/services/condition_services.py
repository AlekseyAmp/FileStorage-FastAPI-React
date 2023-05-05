from models.file import File


async def get_moved_files(condition: str, user_id: str):
    files = []
    async for file in File.find({
        "user_id": user_id
    }):
        if file.metadata[condition]:
            file_dict = {
                "file_id": str(file.id),
                "file_name": file.name,
                "file_size": file.size,
                "file_content_type": file.content_type,
                "file_category_name": file.category_name,
                "is_favorite": file.metadata["is_favorite"],
                "is_basket": file.metadata["is_basket"],
                "date_created": file.metadata["date_created"],
                "time_created": file.metadata["time_created"]
            }
            files.append(file_dict)

    return files[::-1]
