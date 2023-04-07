from constants.category_constants import ALLOWED_FORMATS


def set_file_category(fileformat):
    for category in ALLOWED_FORMATS:
        if fileformat in ALLOWED_FORMATS[category]:
            return category
    return "None"


def is_allowed_format(fileformat, category):
    if fileformat in ALLOWED_FORMATS[category]:
        return True
    return False