from datetime import datetime

from models.statistic import TodayStatistic


async def get_statistic_today(user_id: str):
    statistic_dict = {
        "upload": 0,
        "download": 0,
        "deleted": 0
    }

    statistic_elem = await TodayStatistic.find_one({
        "user_id": user_id,
        "date": datetime.now().strftime("%d-%m-%Y")
    })

    if statistic_elem:
        statistic_dict = {
            "date": statistic_elem.date,
            "upload": statistic_elem.actions.get("upload", 0),
            "download": statistic_elem.actions.get("download", 0),
            "deleted": statistic_elem.actions.get("deleted", 0)
        }

    return statistic_dict


async def set_statistic_today(action: str, user_id: str):
    statistic_elem = await TodayStatistic.find_one({
        "user_id": user_id,
        "date": datetime.now().strftime("%d-%m-%Y")
    })

    if not statistic_elem:
        new_statistic = TodayStatistic(
            user_id=user_id,
            date=datetime.now().strftime("%d-%m-%Y"),
            actions={action: 1}
        )
        await new_statistic.insert()
    else:
        await statistic_elem.update({"$inc":
                                     {f"actions.{action}": 1}})

    return statistic_elem
