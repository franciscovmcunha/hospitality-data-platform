import pandas as pd
import hashlib
from pathlib import Path

# Paths
SOURCE_PATH = Path("data/raw/bookings_expedia.csv")
RAW_PATH = Path("data/raw/bookings_expedia_raw.csv")


def hash_value(value):
    if pd.isna(value):
        return None
    return hashlib.sha256(str(value).encode("utf-8")).hexdigest()


def anonymize_expedia_bookings():
    # Read original Expedia CSV
    df = pd.read_csv(
        SOURCE_PATH,
        sep=",",
        encoding="utf-8"
    )

    # Hash sensitive identifiers
    df["booking_id_hash"] = df["Reservation ID"].apply(hash_value)
    df["confirmation_id_hash"] = df["Confirmation #"].apply(hash_value)

    # Remove PII and raw identifiers
    df = df.drop(
        columns=[
            "Guest",
            "Reservation ID",
            "Confirmation #"
        ],
        errors="ignore"
    )

    # Write anonymized RAW dataset
    df.to_csv(
        RAW_PATH,
        sep=";",
        index=False,
        encoding="utf-8"
    )

    # Remove source file to enforce RAW-only contract
    SOURCE_PATH.unlink()

    # Validation output
    print("✅ Expedia raw dataset anonymized successfully.")
    print(df.shape)
    print(df.columns)


if __name__ == "__main__":
    anonymize_expedia_bookings()
