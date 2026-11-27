from pathlib import Path

# BASE_DIR веде до кореня проєкту Lesson5_coffee_vs_sleep/ (піднімаємося на рівень вище з папки app)
BASE_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = BASE_DIR / "data"
DATA_FILE = DATA_DIR / "work_log.csv"