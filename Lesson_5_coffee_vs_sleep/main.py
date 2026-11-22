from app.data_loader import load_work_log
from app.services import analyze_work_log
from app.exceptions import WorkLogBaseError

def main():
    """Головна точка входу в програму «Дневник программиста на удаленке»."""
    try:
        # Зчитуємо та перевіряємо дані з CSV-файлу
        records = load_work_log()
        
        # Якщо є валідні записи, запускаємо аналіз
        if records:
            analyze_work_log(records)
        else:
            print("Упс! Не знайдено жодного валідного запису для аналізу.")
            
    except WorkLogBaseError as e:
        print(f"[КРИТИЧНА ПОМИЛКА ПРОЄКТУ] {e}")
    except Exception as e:
        print(f"[НЕВІДОМА ПОМИЛКА] Сталася непередбачувана помилка: {e}")

if __name__ == "__main__":
    main()