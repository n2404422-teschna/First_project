WEEK_ORDER = [
    "Понеділок",
    "Вівторок",
    "Середа",
    "Четвер",
    "П'ятниця",
    "Субота",
    "Неділя",
]


def validate_day_entry(hours_slept, coffee_cups):
    """Перевіряє значення сну та кави. Повертає текст помилки або None."""
    if hours_slept < 0 or hours_slept > 24:
        return "Кількість годин сну має бути від 0 до 24."
    if coffee_cups < 0:
        return "Кількість чашок кави не може бути від'ємною."
    return None


def deduplicate_days(records):
    """Прибирає дублікати днів, залишаючи останній запис для кожного дня."""
    by_day = {}
    for row in records:
        by_day[row["day"]] = {
            "day": row["day"],
            "hours_slept": int(row["hours_slept"]),
            "coffee_cups": int(row["coffee_cups"]),
        }

    ordered = []
    for day in WEEK_ORDER:
        if day in by_day:
            ordered.append(by_day[day])

    for row in records:
        day = row["day"]
        if day not in WEEK_ORDER and day in by_day:
            ordered.append(by_day[day])
            del by_day[day]

    return ordered


def filter_records(records, selected_days=None, min_sleep=0):
    """Фільтрує записи за обраними днями та мінімальним сном."""
    result = []
    for row in records:
        if selected_days is not None and row["day"] not in selected_days:
            continue
        if row["hours_slept"] < min_sleep:
            continue
        result.append(row)
    return result


def summarize_records(records):
    """Рахує підсумки за списком записів."""
    count = len(records)
    if count == 0:
        return {
            "days_count": 0,
            "avg_sleep": 0.0,
            "total_coffee": 0,
        }

    total_sleep = 0
    total_coffee = 0

    for row in records:
        total_sleep += int(row["hours_slept"])
        total_coffee += int(row["coffee_cups"])

    return {
        "days_count": count,
        "avg_sleep": round(total_sleep / count, 1),
        "total_coffee": total_coffee,
    }


def get_day_alerts(row):
    """Повертає список попереджень для одного дня."""
    alerts = []
    sleep = int(row["hours_slept"])
    coffee = int(row["coffee_cups"])
    day = str(row["day"])

    if sleep < 3 and coffee == 0:
        alerts.append(
            "🧟 КРИТИЧНИЙ ЗОМБІ-РЕЖИМ: Ви працюєте без палива! Є ризик заснути обличчям на клавіші Backspace і видалити весь проєкт."
        )
    elif sleep < 6:
        alerts.append(
            "💤 УВАГА: Замало сну — організму потрібен відпочинок для відновлення."
        )

    if coffee > 5:
        alerts.append(
            "⚠️ УВАГА: Рівень кофеїну в крові зашкалює! Ви вже чуєте, як компілюється код у сусідній кімнаті. Терміново переходьте на ромашковий чай!"
        )

    if ("П'ятниця" in day or "Friday" in day) and coffee >= 4:
        alerts.append(
            "🚨 П'ЯТНИЧНИЙ ДЕПЛОЙ: Обережно! Кава у п'ятницю ввечері провокує бажання залити сирий код у прод перед вихідними. Відійдіть від кавомашини!"
        )

    return alerts