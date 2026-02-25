import sys
import traceback
from datetime import datetime
from pathlib import Path

# ==========================
# ADD PROJECT ROOT TO PATH
# ==========================

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT))

# ==========================
# IMPORT PIPELINE MODULES
# ==========================

from transformations.staging.stg_bookings import run_staging as run_staging_bookings
from transformations.staging.stg_reviews import run_staging_reviews

from transformations.marts.kpi_bookings import run_gold as run_gold_bookings
from transformations.marts.kpi_reviews import run_gold_reviews

from quality.silver_checks import run_silver_checks


# ==========================
# LOGGER
# ==========================

def log(message: str):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{now}] {message}")


# ==========================
# PIPELINE EXECUTION
# ==========================

def run_pipeline():
    log("🚀 STARTING HOSPITALITY DATA PLATFORM PIPELINE")

    try:
        # -------------------------------------------------
        # SILVER LAYER
        # -------------------------------------------------

        log("🔄 Running Silver Layer - Bookings...")
        run_staging_bookings()
        log("✅ Silver Bookings Completed")

        log("🔄 Running Silver Layer - Reviews...")
        run_staging_reviews()
        log("✅ Silver Reviews Completed")

        # -------------------------------------------------
        # QUALITY CHECKS
        # -------------------------------------------------

        log("🔍 Running Silver Quality Checks (Bookings)...")
        run_silver_checks()
        log("✅ Silver Quality Checks Passed")

        # -------------------------------------------------
        # GOLD LAYER
        # -------------------------------------------------

        log("🏆 Running Gold Layer - Booking KPIs...")
        run_gold_bookings()
        log("✅ Gold Booking KPIs Completed")

        log("🏆 Running Gold Layer - Review KPIs...")
        run_gold_reviews()
        log("✅ Gold Review KPIs Completed")

        log("🎉 PIPELINE FINISHED SUCCESSFULLY")

    except Exception:
        log("❌ PIPELINE FAILED")
        traceback.print_exc()
        sys.exit(1)


# ==========================
# ENTRYPOINT
# ==========================

if __name__ == "__main__":
    run_pipeline()