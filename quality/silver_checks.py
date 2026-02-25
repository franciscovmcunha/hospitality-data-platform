import pandas as pd
from pathlib import Path

SILVER_PATH = Path("data/silver")


def run_silver_checks():
    print("Running Silver Quality Checks...")

    df = pd.read_csv(SILVER_PATH / "stg_bookings.csv")

    errors = []

    valid_booking_dates = df[df["status"] == "OK"]["booking_date"]

    if valid_booking_dates.isnull().any():
        errors.append("Null booking_date found in active bookings")

    # 2️⃣ price >= 0
    if (df["price"] < 0).any():
        errors.append("Negative values found in price")

    # 3️⃣ check_out >= check_in (only for OK bookings)
    valid_df = df[df["status"] == "OK"].copy()

    valid_df["check_in"] = pd.to_datetime(valid_df["check_in"], dayfirst=True, errors="coerce")
    valid_df["check_out"] = pd.to_datetime(valid_df["check_out"], dayfirst=True, errors="coerce")

    if (valid_df["check_out"] < valid_df["check_in"]).any():
        errors.append("check_out earlier than check_in detected")


    # 4️⃣ status allowed values
    allowed_status = ["OK", "Cancelled"]
    if not df["status"].isin(allowed_status).all():
        errors.append("Invalid status values detected")

    if errors:
        print("❌ Silver Checks Failed:")
        for e in errors:
            print("-", e)
        raise Exception("Silver validation failed")

    print("✅ Silver Checks Passed")
