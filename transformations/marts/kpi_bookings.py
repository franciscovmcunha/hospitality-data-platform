import pandas as pd
from pathlib import Path

SILVER_PATH = Path("data/silver")
GOLD_PATH = Path("data/gold")


def run_gold():

    df = pd.read_csv(SILVER_PATH / "stg_bookings.csv")

    df["price"] = pd.to_numeric(df["price"], errors="coerce")

    total_bookings = len(df)
    total_revenue = df["price"].sum()

    cancelled_bookings = len(df[df["status"] == "Cancelled"])
    cancellation_rate = round(cancelled_bookings / total_bookings * 100, 2)

    avg_booking_value = round(df["price"].mean(), 2)

    revenue_by_source = (
        df.groupby("source")["price"]
        .sum()
        .reset_index()
        .rename(columns={"price": "total_revenue"})
    )

    summary = pd.DataFrame({
        "total_bookings": [total_bookings],
        "total_revenue": [round(total_revenue, 2)],
        "cancelled_bookings": [cancelled_bookings],
        "cancellation_rate_percent": [cancellation_rate],
        "avg_booking_value": [avg_booking_value]
    })

    GOLD_PATH.mkdir(parents=True, exist_ok=True)

    summary.to_csv(GOLD_PATH / "kpi_summary.csv", index=False)
    revenue_by_source.to_csv(GOLD_PATH / "revenue_by_source.csv", index=False)

    print("Gold KPIs created successfully.")


if __name__ == "__main__":
    run_gold()