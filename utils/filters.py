from datetime import datetime, timedelta

def filter_by_recency(df, recency):
    if recency == "All":
        return df

    days_map = {
        30: 30,
        60: 60,
        90: 90,
        180: 180
    }

    if recency not in days_map:
        return df

    cutoff = datetime.today() - timedelta(days=days_map[recency])
    return df[df["Trigger Date"] >= cutoff]
