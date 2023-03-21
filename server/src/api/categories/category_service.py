from config.database import GridFSSettings
from api.categories.constants import ALLOWED_FORMATS


grid_fs = GridFSSettings()


def is_allowed_format(fileformat, category):
    if fileformat in ALLOWED_FORMATS[category]:
        return True
    return False


def get_files_by_category(category: str, user_id: str):
    files = []
    for file_obj in grid_fs.file.find():
        if file_obj.metadata["user_id"] == user_id and is_allowed_format(file_obj.fileformat, category):
            file = {
                "file_id": str(file_obj._id),
                "filename": file_obj.filename,
                "fileformat": file_obj.fileformat,
                "content_type": file_obj.content_type,
                "is_favorite": file_obj.metadata["is_favorite"],
                "is_deleted": file_obj.metadata["is_deleted"],
                "upload_date": file_obj.upload_date,
            }
            files.append(file)
    return files
