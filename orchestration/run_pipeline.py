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

from transformations.staging.stg_bookings import run_staging
from transformations.marts.kpi_bookings import run_gold
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
    log("🚀 STARTING DATA PIPELINE")

    try:
        # --------------------------
        #  SILVER (STAGING)
        # --------------------------
        log("🔄 Running Silver (Staging) Layer...")
        run_staging()
        log("✅ Silver Layer Completed")

        # --------------------------
        #  QUALITY CHECKS
        # --------------------------
        log("🔍 Running Silver Quality Checks...")
        run_silver_checks()
        log("✅ Silver Quality Checks Passed")

        # --------------------------
        #  GOLD (MARTS)
        # --------------------------
        log("🏆 Running Gold Layer...")
        run_gold()
        log("✅ Gold Layer Completed")

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