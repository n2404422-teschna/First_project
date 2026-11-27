import sys

print(f"Python version: {sys.version}")

try:
    import pandas as pd
    import numpy as np
    import matplotlib

    print("pandas: OK")
    print("numpy: OK")
    print("matplotlib: OK")
    print("\nВітаємо! Усі бібліотеки встановлено успішно!")
except ImportError as e:
    print(f"\nПомилка: Не вдалося завантажити бібліотеку -> {e}")