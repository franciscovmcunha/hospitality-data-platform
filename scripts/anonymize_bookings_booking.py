# import pandas as pd
# import hashlib
# from datetime import timedelta

# # =========================================================
# # CONFIGURATION
# # =========================================================

# INPUT_PATH = "data/raw/bookings_booking_raw.csv"
# OUTPUT_PATH = "data/raw/bookings_booking_raw.csv"  # overwrite with anonymized version

# # Global date shift (keeps all patterns intact)
# DATE_SHIFT_DAYS = 400

# # Columns containing dates (adjust names if needed)
# DATE_COLUMNS = [
#     "Check-in",
#     "Check-out",
#     "Reservado em",
#     "Data de cancelamento"
# ]

# # Direct PII columns to REMOVE completely
# PII_COLUMNS_TO_DROP = [
#     "Nome do hóspede",
#     "Número de telefone",
#     "Morada",
#     "Comentários"
# ]

# # Columns to HASH (stable identifiers)
# HASH_COLUMNS = {
#     "Número da reserva": "booking_id_hash",
#     "Reservado por": "booker_id_hash"
# }

# # =========================================================
# # HELPERS
# # =========================================================

# def hash_value(value):
#     """
#     Deterministic SHA-256 hash.
#     Same input -> same output.
#     """
#     if pd.isna(value):
#         return None
#     return hashlib.sha256(str(value).encode("utf-8")).hexdigest()


# def shift_date(series, days):
#     """
#     Apply a global date shift to preserve
#     seasonality and relative timing.
#     """
#     return pd.to_datetime(series, errors="coerce") - timedelta(days=days)

# # =========================================================
# # LOAD DATA
# # =========================================================

# df = pd.read_csv(
#     INPUT_PATH,
#     sep=";",
#     encoding="utf-8-sig",
#     engine="python",
#     quotechar='"',
#     escapechar="\\",
#     on_bad_lines="skip"
# )










# # =========================================================
# # HASH IDENTIFIERS
# # =========================================================

# for original_col, hashed_col in HASH_COLUMNS.items():
#     if original_col in df.columns:
#         df[hashed_col] = df[original_col].apply(hash_value)

# # =========================================================
# # DROP DIRECT PII
# # =========================================================

# df = df.drop(columns=[c for c in PII_COLUMNS_TO_DROP if c in df.columns])

# # =========================================================
# # DATE SHIFTING (ANONYMIZATION WITHOUT DATA LOSS)
# # =========================================================

# for col in DATE_COLUMNS:
#     if col in df.columns:
#         df[col] = shift_date(df[col], DATE_SHIFT_DAYS)

# # =========================================================
# # OPTIONAL: AGE BUCKETING (if present)
# # =========================================================

# if "Idade da(s) criança(s)" in df.columns:
#     def bucket_age(age):
#         if pd.isna(age):
#             return None
#         age = int(age)
#         if age <= 5:
#             return "0-5"
#         elif age <= 12:
#             return "6-12"
#         else:
#             return "13+"

#     df["Idade da(s) criança(s)"] = df["Idade da(s) criança(s)"].apply(bucket_age)

# # =========================================================
# # FINAL CLEANUP
# # =========================================================

# # Remove original identifier columns AFTER hashing
# df = df.drop(columns=[c for c in HASH_COLUMNS.keys() if c in df.columns])

# # =========================================================
# # SAVE ANONYMIZED DATA
# # =========================================================

# df.to_csv(OUTPUT_PATH, index=False)

# print("✅ Booking.com raw dataset anonymized successfully.")
# print(df.shape)
# print(df.columns)

import pandas as pd

df = pd.read_csv(
    "data/raw/bookings_booking_raw.csv",
    sep=";",
    encoding="utf-8-sig"
)

df.head(10)
