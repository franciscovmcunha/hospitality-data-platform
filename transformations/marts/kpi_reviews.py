import pandas as pd
from pathlib import Path

SILVER_PATH = Path("data/silver")
GOLD_PATH = Path("data/gold")


def run_gold_reviews():

    df = pd.read_csv(
        SILVER_PATH / "stg_reviews.csv",
        parse_dates=["review_date"]
    )

    # ==========================
    # Global Metrics
    # ==========================

    total_reviews = len(df)
    avg_rating = df["review_rating"].mean()

    review_count_by_source = (
        df.groupby("source")
        .size()
        .reset_index(name="review_count")
    )

    avg_rating_by_source = (
        df.groupby("source")["review_rating"]
        .mean()
        .reset_index(name="avg_rating")
    )

    monthly_review_volume = (
        df.assign(month=df["review_date"].dt.to_period("M"))
        .groupby("month")
        .size()
        .reset_index(name="review_count")
    )

    # ==========================
    # Save Outputs
    # ==========================

    GOLD_PATH.mkdir(parents=True, exist_ok=True)

    # Global summary
    summary_df = pd.DataFrame({
        "total_reviews": [total_reviews],
        "avg_rating": [avg_rating]
    })

    summary_df.to_csv(
        GOLD_PATH / "kpi_reviews_summary.csv",
        index=False
    )

    review_count_by_source.to_csv(
        GOLD_PATH / "kpi_reviews_count_by_source.csv",
        index=False
    )

    avg_rating_by_source.to_csv(
        GOLD_PATH / "kpi_reviews_avg_by_source.csv",
        index=False
    )

    monthly_review_volume.to_csv(
        GOLD_PATH / "kpi_reviews_monthly_volume.csv",
        index=False
    )

    print("Gold Reviews KPIs created successfully.")


if __name__ == "__main__":
    run_gold_reviews()