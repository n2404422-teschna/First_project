from app.data_loader import load_work_log
from app.services import analyze_work_log
from app.exceptions import WorkLogBaseError, DataFileError, InvalidRowError


def main():
    """Головна точка входу в програму «Щоденник програміста на віддаленці — Кава проти Сну»."""
    try:
        # Зчитуємо та перевіряємо дані з CSV-файлу
        records = load_work_log()
        
        # Якщо є валідні записи, запускаємо аналіз
        if records:
            analyze_work_log(records)
        else:
            print("Упс! Не знайдено жодного валідного запису для аналізу.")
            
    except DataFileError as e:
        print(f"[ПОМИЛКА ФАЙЛУ ДАНИХ] {e}")
    except InvalidRowError as e:
        print(f"[ПОМИЛКА В РЯДКУ ДАНИХ] {e}")
    except WorkLogBaseError as e:
        print(f"[КРИТИЧНА ПОМИЛКА ПРОЄКТУ] {e}")
    except (ValueError, ZeroDivisionError) as e:
        print(f"[ПОМИЛКА ОБРОБКИ ДАНИХ] {e}")


if __name__ == "__main__":
    main()