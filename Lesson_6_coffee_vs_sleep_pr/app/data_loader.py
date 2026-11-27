import csv
from app.config import DATA_FILE
from app.exceptions import DataFileError, InvalidRowError


def load_work_log_with_warnings(csv_path=DATA_FILE):
    """Зчитує записи з CSV-файлу та повертає (records, warnings)."""
    if not csv_path.exists():
        raise DataFileError(f"Файл даних не знайдено за шляхом: {csv_path}")

    records = []
    warnings = []

    with open(csv_path, mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        required_columns = ["day", "hours_slept", "coffee_cups", "lines_written"]
        if not reader.fieldnames or any(col not in reader.fieldnames for col in required_columns):
            raise InvalidRowError(
                "У CSV-файлі відсутні потрібні колонки: day, hours_slept, coffee_cups, lines_written."
            )

        for row_idx, row in enumerate(reader, start=1):
            try:
                try:
                    hours_slept = float(row["hours_slept"])
                except (ValueError, TypeError):
                    raise InvalidRowError(
                        f"Рядок {row_idx}: Некоректне значення годин сну -> '{row.get('hours_slept', '')}'"
                    )

                if hours_slept < 0 or hours_slept > 24:
                    raise InvalidRowError(
                        f"Рядок {row_idx}: Недопустима кількість годин сну -> {hours_slept}"
                    )

                try:
                    coffee_cups = int(row["coffee_cups"])
                except (ValueError, TypeError):
                    raise InvalidRowError(
                        f"Рядок {row_idx}: Некоректне значення чашок кави -> '{row.get('coffee_cups', '')}'"
                    )

                if coffee_cups < 0:
                    raise InvalidRowError(
                        f"Рядок {row_idx}: Кількість кави не може бути від'ємною -> {coffee_cups}"
                    )

                try:
                    lines_written = int(row["lines_written"])
                except (ValueError, TypeError):
                    raise InvalidRowError(
                        f"Рядок {row_idx}: Некоректна кількість рядків коду -> '{row.get('lines_written', '')}'"
                    )

                if lines_written < 0:
                    raise InvalidRowError(
                        f"Рядок {row_idx}: Кількість рядків коду не може бути від'ємною -> {lines_written}"
                    )

                records.append({
                    "day": row["day"],
                    "hours_slept": hours_slept,
                    "coffee_cups": coffee_cups,
                    "lines_written": lines_written,
                })

            except InvalidRowError as err:
                warnings.append(str(err))

    return records, warnings


def load_work_log(csv_path=DATA_FILE):
    """Зчитує валідні записи з CSV-файлу (збережено для сумісності з main.py)."""
    records, warnings = load_work_log_with_warnings(csv_path)
    for warning in warnings:
        print(f"[ПОПЕРЕДЖЕННЯ У ДАНИХ] {warning}")
    return records