from datetime import datetime
from models.history import History


async def get_all_history(user_id: str):
    history = {}

    async for history_elem in History.find({
        "user_id": user_id
    }):
        date = history_elem.date
        history[date] = []
        for history_list_elem in history_elem.history_list:
            # Пропуск категории по умолчанию
            if "default_category" in history_list_elem["description"]:
                continue

            history_dict = {
                "title": history_list_elem["title"],
                "description": history_list_elem["description"],
                "time": history_list_elem["time"]
            }
            history[date].append(history_dict)

    # Сортировка ключей словаря, для вывода дат снизу вверх
    history = {key: history[key] for key in sorted(history, reverse=True)}

    return history


async def get_last_five_history(user_id: str):
    history = []

    async for history_elem in History.find({
        "user_id": user_id,
        "date": datetime.now().strftime("%d-%m-%Y"),
    }):
        for history_list_elem in history_elem.history_list[0:6]:

            """
            Пояснение блока с 55стр. - 62стр.:

            Если поле "category_name" есть и его значение отличается
            от "default_category",
            то записывает это значение в переменную "name".

            Если поле "category_name" отсутствует, то проверяет, 
            есть ли в словаре поле "file_name". Если оно есть,
            то записывает его значение в переменную "name".

            Если поля "category_name" и "file_name" нет,
            то записывает значение поля "title" в переменную "name".
            """

            if history_list_elem.get("category_name"):
                if history_list_elem["category_name"] == "default_category":
                    continue
                name = history_list_elem["category_name"]
            elif history_list_elem.get("file_name"):
                name = history_list_elem["file_name"]
            else:
                name = history_list_elem["title"]

            history_dict = {
                "name": name,
                "title": history_list_elem["title"],
                "description": history_list_elem["description"],
                "date": history_elem.date,
                "time": history_list_elem["time"]
            }
            history.append(history_dict)

    return history


async def set_history_today(history_dict: dict, user_id: str):
    history_elem = await History.find_one({
        "user_id": user_id,
        "date": datetime.now().strftime("%d-%m-%Y")
    })

    """
    Пояснение блока с 93стр. - 101стр.:

    Если элемент истории для текущей даты уже существует, 
    то новый элемент добавляется в начало списка истории.

    Если же элементов истории на текущую дату еще нет,
    то создается новый документ в коллекции историй с новым списком историй,
    содержащим только переданный элемент.
    """

    if not history_elem:
        new_history = History(
            user_id=user_id,
            history_list=[history_dict]
        )
        await new_history.insert()
    else:
        history_elem.history_list.insert(0, history_dict)
        await history_elem.save()

    return history_elem
