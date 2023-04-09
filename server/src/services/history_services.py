from fastapi import HTTPException
from datetime import datetime


async def get_history(model, user_id: str):
    history = []
    async for history_elem in model.find():
        if history_elem.user_id == user_id:
             history.append(history_elem)
    return history


async def get_history_files_today(model, user_id: str):
    today = datetime.now().strftime("%d-%m-%Y")
    history_elem = await model.find_one({'user_id': user_id, 'date': today})
    
    if not history_elem:
        raise HTTPException(status_code=404, detail="Запись истории не найдена")
    
    return history_elem
