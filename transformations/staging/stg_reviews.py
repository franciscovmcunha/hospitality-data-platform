import pandas as pd
import csv
from pathlib import Path
import re

BRONZE_PATH = Path("data/bronze")
SILVER_PATH = Path("data/silver")


# ==========================
# Helpers
# ==========================

def parse_booking_rating(series):
    return pd.to_numeric(series, errors="coerce")


def parse_expedia_rating(series):
    # Extract number from "10 out of 10"
    return (
        series.astype(str)
        .str.extract(r"(\d+(?:\.\d+)?)")[0]
        .astype(float)
    )


def clean_text(series):
    return series.fillna("").astype(str).str.strip()


# ==========================
# Booking Transformation
# ==========================

def transform_booking_reviews(df):
    df_copy = df.copy()

    df_copy["review_date"] = pd.to_datetime(
        df_copy["Data do comentário"],
        errors="coerce"
    )

    df_copy["review_rating"] = parse_booking_rating(
        df_copy["Pontuação de comentários"]
    )

    df_copy["review_title"] = clean_text(
        df_copy["Título do comentário"]
    )

    positive = clean_text(df_copy["Comentário positivo"])
    negative = clean_text(df_copy["Comentário negativo"])

    df_copy["review_text"] = (
        positive + 
        ("\n\nNegative: " + negative).where(negative != "", "")
    )

    df_copy["review_response"] = clean_text(
        df_copy["Resposta do alojamento"]
    )

    df_copy["source"] = "booking"

    return df_copy[
        [
            "review_date",
            "review_rating",
            "review_title",
            "review_text",
            "review_response",
            "source",
        ]
    ]


# ==========================
# Expedia Transformation
# ==========================

def transform_expedia_reviews(df):
    df_copy = df.copy()

    df_copy["review_date"] = pd.to_datetime(
        df_copy["review_date"],
        errors="coerce"
    )

    df_copy["review_rating"] = parse_expedia_rating(
        df_copy["review_rating"]
    )

    df_copy["review_title"] = clean_text(
        df_copy["review_title"]
    )

    df_copy["review_text"] = clean_text(
        df_copy["review_text"]
    )

    df_copy["review_response"] = clean_text(
        df_copy["review_response"]
    )

    # Normalize brand_type
    df_copy["source"] = "expedia"

    return df_copy[
        [
            "review_date",
            "review_rating",
            "review_title",
            "review_text",
            "review_response",
            "source",
        ]
    ]


# ==========================
# Run Staging
# ==========================

def run_staging_reviews():

    booking_df = pd.read_csv(
        BRONZE_PATH / "reviews_booking_bronze.csv",
        encoding="utf-8"
    )
   
    expedia_df = pd.read_csv(
        BRONZE_PATH / "reviews_expedia_bronze.csv",
        encoding="utf-8",
        sep=",",
        engine="python",
        quotechar='"'
    )

    print("Expedia columns detected:", expedia_df.columns.tolist())


    booking_silver = transform_booking_reviews(booking_df)
    expedia_silver = transform_expedia_reviews(expedia_df)

    final_df = pd.concat(
        [booking_silver, expedia_silver],
        ignore_index=True
    )

    SILVER_PATH.mkdir(parents=True, exist_ok=True)

    final_df.to_csv(
        SILVER_PATH / "stg_reviews.csv",
        index=False,
        encoding="utf-8",
        quoting=csv.QUOTE_ALL
    )

    print("Silver Reviews layer created successfully.")
    print("Final shape:", final_df.shape)


if __name__ == "__main__":
    run_staging_reviews()