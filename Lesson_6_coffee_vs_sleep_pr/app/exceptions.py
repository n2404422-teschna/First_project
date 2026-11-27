class WorkLogBaseError(Exception):
    """Базовий клас для всіх помилок нашого проєкту."""
    pass

class DataFileError(WorkLogBaseError):
    """Помилка, коли файл з даними не знайдено або пошкоджений."""
    pass

class InvalidRowError(WorkLogBaseError):
    """Помилка у конкретному рядку даних (неправильний формат, від'ємні числа тощо)."""
    pass