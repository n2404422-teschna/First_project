import csv
from app.config import DATA_FILE
from app.exceptions import DataFileError, InvalidRowError

def load_work_log():
    """Зчитує дані з CSV-файлу та перевіряє їх на наявність помилок."""
    if not DATA_FILE.exists():
        raise DataFileError(f"Файл даних не знайдено за шляхом: {DATA_FILE}")

    records = []
    
    with open(DATA_FILE, mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        
        for row_idx, row in enumerate(reader, start=1):
            try:
                # Перевірка та перетворення годин сну
                try:
                    hours_slept = float(row["hours_slept"])
                except ValueError:
                    raise InvalidRowError(f"Рядок {row_idx}: Некоректне значення годин сну -> '{row['hours_slept']}'")

                # Перевірка на нереальну кількість годин сну
                if hours_slept < 0 or hours_slept > 24:
                    raise InvalidRowError(f"Рядок {row_idx}: Недопустима кількість годин сну -> {hours_slept}")

                # Перевірка та перетворення чашок кави
                try:
                    coffee_cups = int(row["coffee_cups"])
                except ValueError:
                    raise InvalidRowError(f"Рядок {row_idx}: Некоректне значення чашок кави -> '{row['coffee_cups']}'")

                if coffee_cups < 0:
                    raise InvalidRowError(f"Рядок {row_idx}: Кількість кави не може бути від'ємною -> {coffee_cups}")

                # Перевірка рядків коду
                try:
                    lines_written = int(row["lines_written"])
                except ValueError:
                    raise InvalidRowError(f"Рядок {row_idx}: Некоректна кількість рядків коду -> '{row['lines_written']}'")

                # Додаємо валідний запис до списку
                records.append({
                    "day": row["day"],
                    "hours_slept": hours_slept,
                    "coffee_cups": coffee_cups,
                    "lines_written": lines_written
                })

            except InvalidRowError as e:
                print(f"[ПОПЕРЕДЖЕННЯ У ДАНИХ] {e}")

    return records