import pandas as pd
import hashlib
import csv
import unicodedata
from pathlib import Path

# ------------------------------------------
# Paths                 
# ------------------------------------------

RAW_PATH = Path("data/raw")

BRONZE_PATH = Path("data/bronze")

# ------------------------------------------
# Helpers                 
# ------------------------------------------

def hash_value(value):
    if pd.isna(value):
        return value
    return hashlib.sha256(str(value).encode("utf-8")).hexdigest()

def normalize(text):
    text = str(text).strip().lower()
    text = unicodedata.normalize("NFKD", text)
    text = text.encode("Ascii", "ignore").decode("utf-8")
    return text

def detect_delimiter(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        sample = f.read(5000)
        sniffer = csv.Sniffer()
        dialect = sniffer.sniff(sample)
        return dialect.delimiter

# -------------------------------------------------
# Anonymization 
# -------------------------------------------------

SENSITIVE_COLUMNS = [
    "Guest",
    "Reservation ID",
    "Confirmation #",
    "review_by",
    "review_response_by"
]

def anonymization_dataframe(df: pd.DataFrame) -> pd.DataFrame:

    df_copy = df.copy()
    
    normalized_columns = {
        normalize(col): col for col in df_copy.columns
    }

    for sensitive in SENSITIVE_COLUMNS:
        normalized_sensitive = normalize(sensitive)

        if normalized_sensitive in normalized_columns:
            original_col = normalized_columns[normalized_sensitive]
            print(f"Anonymizing Column: {original_col}")
            df_copy[original_col] = df_copy[original_col].apply(hash_value)

    return df_copy

# -------------------------------------------------
# Bronze Transformations
# -------------------------------------------------

# -------------------------------------------------
# Bronze Transformations
# -------------------------------------------------

def transform_bronze(df: pd.DataFrame) -> pd.DataFrame:

    df_copy = df.copy()

    for col in df_copy.columns:
        normalized_col = normalize(col)

        if any(keyword in normalized_col for keyword in ["check-in", "check-out", "booked", "date"]):

            df_copy[col] = df_copy[col].astype(str).str.replace("/", "-", regex=False)

            df_copy[col] = pd.to_datetime(
                df_copy[col],
                errors="coerce",
                utc=True 
            )

            df_copy[col] = df_copy[col].dt.tz_convert(None)
            df_copy[col] = df_copy[col].dt.strftime("%d-%m-%Y")

    return df_copy

# -------------------------------------------------
# Process file
# -------------------------------------------------

def process_file(filename: str):

    raw_file = RAW_PATH / filename
    bronze_filename = filename.replace("_raw", "_bronze")
    bronze_file = BRONZE_PATH / bronze_filename

    print(f"\nProcessing: {filename}")

    if "bookings" in filename:
        sep = ";"
    else:
        sep = ","
    
    if "reviews" in filename:
        df = pd.read_csv(
        raw_file,
        sep="\t",          
        encoding="utf-8"
    )
    else:
        df = pd.read_csv(
        raw_file,
        sep=";",
        encoding="utf-8"
    )

    print("Columns detected:", df.columns.tolist())
    print("Shape:", df.shape)

    df_anonymized = anonymization_dataframe(df)
    df_bronze = transform_bronze(df_anonymized)

    BRONZE_PATH.mkdir(parents=True, exist_ok=True)
    df_bronze.to_csv(bronze_file, index=False)

    print("Shape after:", df_bronze.shape)
    print(f"Saved bronze file to: {bronze_file}")

# -------------------------------------------------
# Main
# -------------------------------------------------

if __name__ == "__main__":
    files = [
        "bookings_expedia_raw.csv",
        "reviews_expedia_raw.csv"
    ]

    for file in files:
        process_file(file)



