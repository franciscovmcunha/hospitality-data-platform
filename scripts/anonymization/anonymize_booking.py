import pandas as pd
import hashlib
import csv
import unicodedata
from pathlib import Path

# -------------------------------------------------
# Paths
# -------------------------------------------------

RAW_PATH = Path("data/raw")
BRONZE_PATH = Path("data/bronze")

# -------------------------------------------------
# Helpers
# -------------------------------------------------

def hash_value(value):
    if pd.isna(value):
        return value
    return hashlib.sha256(str(value).encode("utf-8")).hexdigest()


def normalize(text):
    text = str(text).strip().lower()
    text = unicodedata.normalize("NFKD", text)
    text = text.encode("ascii", "ignore").decode("utf-8")
    return text


def detect_delimiter(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        sample = f.read(5000)
        sniffer = csv.Sniffer()
        dialect = sniffer.sniff(sample)
        return dialect.delimiter

# -------------------------------------------------
# Anonymization (safe & controlled)
# -------------------------------------------------

SENSITIVE_COLUMNS = [
    "Número da reserva",
    "Reservado por",
    "Nome do Hóspede",
    "Morada",
    "Número de telefone",
    "Email"
]

def anonymize_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    df_copy = df.copy()

    normalized_columns = {
        normalize(col): col for col in df_copy.columns
    }

    for sensitive in SENSITIVE_COLUMNS:
        normalized_sensitive = normalize(sensitive)

        if normalized_sensitive in normalized_columns:
            original_col = normalized_columns[normalized_sensitive]
            print(f"Anonymizing column: {original_col}")
            df_copy[original_col] = df_copy[original_col].apply(hash_value)

    return df_copy

# -------------------------------------------------
# Bronze Transformations
# -------------------------------------------------

def transform_bronze(df: pd.DataFrame) -> pd.DataFrame:
    df_copy = df.copy()

    # 1️⃣ Uppercase country
    for col in df_copy.columns:
        normalized_col = normalize(col)
        if "country" in normalized_col or "pais" in normalized_col:
            df_copy[col] = df_copy[col].astype(str).str.upper()

    # 2️⃣ Normalize dates (DD-MM-YYYY)
    for col in df_copy.columns:
        normalized_col = normalize(col)
        if "data" in normalized_col or "date" in normalized_col:
            df_copy[col] = pd.to_datetime(df_copy[col], errors="coerce")
            df_copy[col] = df_copy[col].dt.strftime("%d-%m-%Y")

    # 3️⃣ Clean monetary values (Preço / Valor / Total etc)
    for col in df_copy.columns:
        normalized_col = normalize(col)

        if any(keyword in normalized_col for keyword in ["valor", "price", "total", "amount", "preco"]):
            print(f"Cleaning monetary column: {col}")

            df_copy[col] = (
                df_copy[col]
                .astype(str)
                .str.replace("EUR", "", regex=False)
                .str.replace("€", "", regex=False)
                .str.replace(" ", "", regex=False)
                .str.replace(",", ".", regex=False)
            )

            df_copy[col] = pd.to_numeric(df_copy[col], errors="coerce")

    return df_copy

# -------------------------------------------------
# Process file
# -------------------------------------------------

def process_file(filename: str):
    raw_file = RAW_PATH / filename
    bronze_filename = filename.replace("_raw", "_bronze")
    bronze_file = BRONZE_PATH / bronze_filename

    print(f"\nProcessing: {filename}")

    delimiter = detect_delimiter(raw_file)
    print(f"Detected delimiter: '{delimiter}'")

    df = pd.read_csv(
        raw_file,
        sep=delimiter,
        encoding="utf-8",
        engine="python"
    )

    # Step 1: Anonymize
    df_anonymized = anonymize_dataframe(df)

    # Step 2: Bronze transformations
    df_bronze = transform_bronze(df_anonymized)

    BRONZE_PATH.mkdir(parents=True, exist_ok=True)
    df_bronze.to_csv(bronze_file, index=False)

    print(f"Saved bronze file to: {bronze_file}")

# -------------------------------------------------
# Main
# -------------------------------------------------

if __name__ == "__main__":
    files = [
        "bookings_booking_raw.csv",
        "reviews_booking_raw.csv"
    ]

    for file in files:
        process_file(file)