from typing import Any
from datetime import datetime
from models.history import FileHistory, UserHistory


async def get_files_history(user_id: str):
    history = {}
    async for history_elem in FileHistory.find({
        "user_id": user_id
    }):
        date = history_elem.date
        history[date] = []
        for history_list_elem in history_elem.history_list:
            history_dict = {
                "file_id": history_list_elem["file_id"],
                "title": history_list_elem["title"],
                "description": history_list_elem["description"],
                "time": history_list_elem["time"]
            }
            history[date].insert(0, history_dict)

    return history


async def get_last_five_files_history(user_id: str):
    history = []
    async for history_elem in FileHistory.find({
        "user_id": user_id,
    }):
        for history_list_elem in history_elem.history_list[-1:-6:-1]:
            history_dict = {
                "file_id": history_list_elem["file_id"],
                "file_name": history_list_elem["file_name"],
                "file_contentType": history_list_elem["file_contentType"],
                "title": history_list_elem["title"],
                "description": history_list_elem["description"],
                "date": history_elem.date,
                "time": history_list_elem["time"]
            }
            history.append(history_dict)

    return history



async def get_user_history(user_id: str):
    history = {}
    async for history_elem in UserHistory.find({
        "user_id": user_id
    }):
        date = history_elem.date
        history[date] = []
        for history_list_elem in history_elem.history_list:
            history_dict = {
                "title": history_list_elem["title"],
                "description": history_list_elem["description"],
                "time": history_list_elem["time"]
            }
            history[date].insert(0, history_dict)

    return history


async def set_history_today(model: Any, history_dict: dict, user_id: str):
    history_elem = await model.find_one({
        "user_id": user_id,
        "date": datetime.now().strftime("%d-%m-%Y")
    })

    if not history_elem:
        new_history = model(
            user_id=user_id,
            history_list=[history_dict]
        )
        await new_history.insert()
    else:
        history_elem.history_list.append(history_dict)
        await history_elem.save()

    return history_elem
