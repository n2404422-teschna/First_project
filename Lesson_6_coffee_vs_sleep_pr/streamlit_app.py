import pandas as pd
import streamlit as st

from app.services import (
    WEEK_ORDER,
    deduplicate_days,
    filter_records,
    get_day_alerts,
    summarize_records,
    validate_day_entry,
)

st.set_page_config(page_title="Аналіз дня програміста: кава проти сну", layout="wide")

st.title("АНАЛІЗ ДНЯ ПРОГРАМІСТА: КАВА ПРОТИ СНУ")
st.write(
    "Додавайте дні тижня по одному (сон у цілих годинах та кількість чашок кави), закріплюйте їх у таблиці та переглядайте підсумки, графік і попередження."
)

if "week_records" not in st.session_state:
    st.session_state.week_records = []

if "entry_error" not in st.session_state:
    st.session_state.entry_error = None

if "min_sleep_filter" not in st.session_state:
    st.session_state.min_sleep_filter = 0

week_records = st.session_state.week_records

st.subheader("Додати або оновити день (1 тиждень)")

c1, c2, c3 = st.columns(3)
with c1:
    chosen_day = st.selectbox("День тижня", options=WEEK_ORDER)
with c2:
    chosen_sleep = st.number_input("Сон (год)", value=7, step=1)
with c3:
    chosen_coffee = st.number_input("Кава (чашок)", value=2, step=1)

b1, b2 = st.columns([1, 1])
with b1:
    if st.button("Перевірити і закріпити"):
        err_msg = validate_day_entry(chosen_sleep, chosen_coffee)
        if err_msg is not None:
            st.session_state.entry_error = err_msg
        else:
            st.session_state.entry_error = None
            new_list = list(week_records)
            new_list.append({
                "day": chosen_day,
                "hours_slept": int(chosen_sleep),
                "coffee_cups": int(chosen_coffee),
            })
            st.session_state.week_records = deduplicate_days(new_list)
            st.session_state[f"chk_{chosen_day}"] = True
        st.rerun()

with b2:
    if st.button("Очистити тиждень"):
        st.session_state.week_records = []
        st.session_state.entry_error = None
        st.rerun()

if st.session_state.entry_error:
    st.error(st.session_state.entry_error)

st.sidebar.header("Фільтри")

if st.sidebar.button("Скинути фільтри"):
    for row in week_records:
        st.session_state[f"chk_{row['day']}"] = True
    st.session_state.min_sleep_filter = 0
    st.rerun()

st.sidebar.write("**Відстежувані дні:**")

selected_days = []
for row in week_records:
    day_name = row["day"]
    chk_key = f"chk_{day_name}"
    if chk_key not in st.session_state:
        st.session_state[chk_key] = True
    checked = st.sidebar.checkbox(day_name, key=chk_key)
    if checked:
        selected_days.append(day_name)

min_sleep_filter = st.sidebar.slider(
    "Мінімум сну у вибірці (год)",
    min_value=0,
    max_value=24,
    step=1,
    key="min_sleep_filter",
)

if not week_records:
    st.info("Додайте перший день вище та натисніть «Перевірити і закріпити».")
    st.stop()

filtered = filter_records(
    week_records,
    selected_days=selected_days,
    min_sleep=min_sleep_filter,
)

if not filtered:
    st.warning("За обраними фільтрами немає записів. Натисніть «Скинути фільтри» або змініть умови.")
    st.stop()

summary = summarize_records(filtered)

st.subheader("Підсумки")
m1, m2, m3 = st.columns(3)
m1.metric("Днів у вибірці", summary["days_count"])
m2.metric("Середній сон, год", summary["avg_sleep"])
m3.metric("Усього кави, чашок", summary["total_coffee"])

df = pd.DataFrame([
    {
        "День": row["day"],
        "Сон (год)": int(row["hours_slept"]),
        "Кава (чашок)": int(row["coffee_cups"]),
    }
    for row in filtered
])

st.subheader("Таблиця за тиждень")
st.dataframe(df)

st.subheader("Графік за днями")
metric_choice = st.radio(
    "Що показати на графіку",
    options=["Кава (чашок)", "Сон (год)"],
    horizontal=True,
)
st.bar_chart(df.set_index("День")[[metric_choice]])

st.subheader("Попередження")
found_alerts = False
for row in filtered:
    day_alerts = get_day_alerts(row)
    if day_alerts:
        found_alerts = True
        for alert in day_alerts:
            st.warning(
                f"День: {row['day']} | Сон: {row['hours_slept']} год | Кава: {row['coffee_cups']} чаш. — {alert}"
            )

if not found_alerts:
    st.info("Попереджень за обраними днями немає.")