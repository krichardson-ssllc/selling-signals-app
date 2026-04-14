import pandas as pd
from datetime import datetime

def normalize_employees(value):
    if pd.isna(value):
        return None
    if isinstance(value, (int, float)):
        return value
    if "–" in value or "-" in value:
        parts = value.replace("–", "-").split("-")
        try:
            return int((int(parts[0]) + int(parts[1])) / 2)
        except Exception:
            return None
    return None


def assign_calendar_bucket(trigger_date):
    if trigger_date is None or pd.isna(trigger_date):
        return "Unknown"

    today = datetime.today()
    days_ago = (today - trigger_date).days

    if days_ago <= 7:
        return "This Week"
    elif days_ago <= 14:
        return "Last 2 Weeks"
    elif trigger_date.month == today.month and trigger_date.year == today.year:
        return "This Month"
    else:
        return "Older"


def load_and_prepare_data(path):
    df = pd.read_csv(path)

    # If schema-only CSV, return empty DataFrame safely
    if df.empty:
        return df

    df["Employee Count"] = df.get("Employees", None).apply(normalize_employees)

    df["Trigger Date"] = pd.to_datetime(
        df.get("Trigger Date", None),
        errors="coerce"
    )

    df["Call Timing"] = df["Trigger Date"].apply(assign_calendar_bucket)

    return df
``
