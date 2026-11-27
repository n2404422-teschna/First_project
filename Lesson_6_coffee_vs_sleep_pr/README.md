# Аналіз дня програміста: кава проти сну

Додаток допомагає людині з щільним графіком відстежувати сон та кількість випитих чашок кави по днях тижня, щоб вчасно помічати недосип і надлишок кофеїну.

## Як запустити локально

python -m venv .venv
.venv\Scripts\activate
python -m pip install -r requirements.txt
streamlit run streamlit_app.py

## Тести

python -m pytest -v

## Онлайн-версія

https://cofffeevssleep.streamlit.app/