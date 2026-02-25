import pandas as pd
from pathlib import Path

BRONZE_PATH = Path("data/bronze")

ALLOWED_STATUS = ["postStay", "cancelled", "confirmed"]

def check_nulls(df, filename):
    print(f"\nChecking null values for {filename}")
    null_counts = df.isnull().sum()
    print(null_counts[null_counts > 0])


def check_negative_amounts(df, filename):
    for col in df.columns:
        if "amount" in col.lower() or "price" in col.lower():
            if (df[col] < 0).any():
                print(f"Negative values detected in {col} ({filename})")


def check_status(df, filename):
    for col in df.columns:
        if "status" in col.lower():
            invalid = df[~df[col].isin(ALLOWED_STATUS)]
            if not invalid.empty:
                print(f"Invalid status detected in {filename}")
                print(invalid[col].unique())


def check_dates(df, filename):
    for col in df.columns:
        if "date" in col.lower() or "check" in col.lower():
            invalid_dates = pd.to_datetime(df[col], errors="coerce").isnull()
            if invalid_dates.any():
                print(f"Invalid date format detected in column {col} ({filename})")


def run_checks():
    files = list(BRONZE_PATH.glob("*.csv"))

    for file in files:
        print(f"\nRunning quality checks on {file.name}")
        df = pd.read_csv(file)

        check_nulls(df, file.name)
        check_negative_amounts(df, file.name)
        check_status(df, file.name)
        check_dates(df, file.name)

    print("\nQuality checks completed.")


if __name__ == "__main__":
    run_checks()