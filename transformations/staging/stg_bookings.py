import pandas as pd
from pathlib import Path

BRONZE_PATH = Path("data/bronze")
SILVER_PATH = Path("data/silver")


# ==========================
# DATE PARSER (ROBUST)
# ==========================

def format_date(series):
    return (
        pd.to_datetime(series, errors="coerce", utc=True)
        .dt.tz_convert(None)
    )


# ==========================
# BOOKING TRANSFORMATION
# ==========================

def transform_booking(df):
    df_copy = df.copy()

    df_copy["booking_date"] = format_date(df_copy["Reservado em"])
    df_copy["check_in"] = format_date(df_copy["Check-in"])
    df_copy["check_out"] = format_date(df_copy["Check-out"])

    df_copy["price"] = pd.to_numeric(df_copy["Preço"], errors="coerce")

    df_copy["status"] = (
    df_copy["Estado"]
    .astype(str)
    .str.strip()
    .str.lower()
)

    df_copy["status"] = df_copy["status"].map({
    "ok": "OK",
    "inhouse": "OK",
    "in_house": "OK",
    "cancelled_by_guest": "Cancelled",
    "cancelled_by_hotel": "Cancelled",
    "no_show": "Cancelled"
    }).fillna("Cancelled")

    df_copy["booker_country"] = df_copy["Booker country"]
    df_copy["cancelling_date"] = format_date(df_copy["Data de cancelamento"])

    df_copy["source"] = "booking"

    return df_copy[
        [
            "booking_date",
            "check_in",
            "check_out",
            "price",
            "status",
            "booker_country",
            "cancelling_date",
            "source",
        ]
    ]


# ==========================
# EXPEDIA TRANSFORMATION
# ==========================

def transform_expedia(df):
    df_copy = df.copy()

    df_copy["booking_date"] = format_date(df_copy["Booked"])
    df_copy["check_in"] = format_date(df_copy["Check-in"])
    df_copy["check_out"] = format_date(df_copy["Check-out"])

    df_copy["booking_date"] = df_copy["booking_date"].fillna(df_copy["check_in"])

    mask = df_copy["check_out"] < df_copy["check_in"]

    df_copy.loc[mask, ["check_in", "check_out"]] = (
    df_copy.loc[mask, ["check_out", "check_in"]].values
)
    df_copy["price"] = pd.to_numeric(df_copy["Booking amount"], errors="coerce")

    df_copy["status"] = (
    df_copy["Status"]
    .astype(str)
    .str.strip()
    .str.lower()
    .replace({
        "poststay": "OK",
        "cancelled": "Cancelled",
        "inhouse": "OK",
        "in_house": "OK",
         "no_show": "Cancelled"

    })
)

    df_copy["booker_country"] = None
    df_copy["cancelling_date"] = None

    df_copy["source"] = "expedia"

    return df_copy[
        [
            "booking_date",
            "check_in",
            "check_out",
            "price",
            "status",
            "booker_country",
            "cancelling_date",
            "source",
        ]
    ]


# ==========================
# RUN STAGING
# ==========================

def run_staging():

    booking_df = pd.read_csv(BRONZE_PATH / "bookings_booking_bronze.csv")
    expedia_df = pd.read_csv(BRONZE_PATH / "bookings_expedia_bronze.csv")

    booking_silver = transform_booking(booking_df)
    expedia_silver = transform_expedia(expedia_df)

    final_df = pd.concat([booking_silver, expedia_silver], ignore_index=True)

    SILVER_PATH.mkdir(parents=True, exist_ok=True)
    final_df.to_csv(SILVER_PATH / "stg_bookings.csv", index=False)

    print("Silver layer created successfully.")
    print("Final shape:", final_df.shape)


if __name__ == "__main__":
    run_staging()