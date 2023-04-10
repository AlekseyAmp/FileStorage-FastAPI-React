from constants.category_constants import ALLOWED_FORMATS


def set_file_category(fileformat: str):
    for category in ALLOWED_FORMATS:
        if fileformat in ALLOWED_FORMATS[category]:
            return category
    return False


def is_allowed_format(fileformat: str, category: str):
    if fileformat in ALLOWED_FORMATS[category]:
        return True
    return False
