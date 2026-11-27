def analyze_work_log(records):
    """Аналізує записи про сон і каву та виводить життєві попередження для програміста."""
    total_coffee = 0
    total_sleep = 0
    total_lines = 0
    days_count = len(records)

    print("\n--- АНАЛІЗ ДНЯ ПРОГРАМІСТА: КОФЕ ПРОТИ СНА ---")
    
    for record in records:
        day = record["day"]
        sleep = record["hours_slept"]
        coffee = record["coffee_cups"]
        lines = record["lines_written"]

        total_coffee += coffee
        total_sleep += sleep
        total_lines += lines

        print(f"\nДень: {day} | Сон: {sleep} год | Кава: {coffee} чаш. | Код: {lines} рядків")

        # 1. Попередження про «кофейний передоз» (більше 5 чашок кави)
        if coffee > 5:
            print("  ⚠️ Рівень кофеїну в крові зашкалює! Ви вже чуєте, як компілюється код у сусідній кімнаті. Терміново переходьте на ромашковий чай!")

        # 2. Попередження для «ночного зомби» (сон менше 3 годин і 0 чашок кави)
        if sleep < 3 and coffee == 0:
            print("  🧟 КРИТИЧНИЙ ЗОМБІ-РЕЖИМ: Ви працюєте без палива! Є ризик заснути обличчям на клавіші Backspace і видалити весь проєкт.")

        # 3. Попередження про п'ятничний деплой (якщо це п'ятниця і багато кави)
        if "Friday" in day and coffee >= 4:
            print("  🚨 П'ЯТНИЧНИЙ ДЕПЛОЙ: Обережно! Кава у п'ятницю ввечері провокує бажання залити сирий код у прод перед вихідними. Відійдіть від кавомашини!")

    try:
        avg_coffee = total_coffee / days_count
    except ZeroDivisionError:
        avg_coffee = 0.0
        print("\n[ПОПЕРЕДЖЕННЯ] Немає записів для обчислення середньої кількості чашок кави.")

    if days_count > 0:
        print("\n--- ПІДСУМКИ ТИЖНЯ ---")
        print(f"Середній сон: {total_sleep / days_count:.1f} год/день")
        print(f"Загалом випито кави: {total_coffee} чашок (у середньому {avg_coffee:.1f} чаш./день)")
        print(f"Загалом написано рядків коду: {total_lines}")