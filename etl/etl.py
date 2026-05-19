import requests
import pandas as pd
import logging
import time

from tenacity import (
    retry,
    stop_after_attempt,
    wait_fixed
)

from models import MarketData
from db import engine


# ----------------------------------
# Logging Configuration
# ----------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


# ----------------------------------
# API URL
# ----------------------------------

API_URL = "http://api:8000/v1/market-data"


# ----------------------------------
# Retry Configuration
# ----------------------------------

@retry(
    stop=stop_after_attempt(3),
    wait=wait_fixed(2)
)
def fetch_market_data():

    response = requests.get(
        API_URL,
        timeout=5
    )

    response.raise_for_status()

    return response.json()


# ----------------------------------
# Start Execution Timer
# ----------------------------------

start_time = time.time()


# ----------------------------------
# Extract
# ----------------------------------

try:

    data = fetch_market_data()

except Exception as e:

    logging.error(
        f"API Extraction Failed: {e}"
    )

    raise SystemExit()


# ----------------------------------
# Validation
# ----------------------------------

validated_records = []

dropped_records = 0


for record in data:

    try:

        validated = MarketData(**record)

        validated_records.append(
            validated.model_dump()
        )

    except Exception as e:

        dropped_records += 1

        logging.error(
            f"Validation Failed: {e}"
        )


# ----------------------------------
# Convert To DataFrame
# ----------------------------------

df = pd.DataFrame(validated_records)


# ----------------------------------
# Exit If No Valid Data
# ----------------------------------

if df.empty:

    logging.warning(
        "No valid records available"
    )

    raise SystemExit()


# ----------------------------------
# VWAP Calculation
# ----------------------------------

df["price_volume"] = (
    df["price"] * df["volume"]
)

vwap_df = (
    df.groupby("instrument_id")
    .apply(
        lambda x:
        x["price_volume"].sum()
        / x["volume"].sum()
    )
    .reset_index(name="vwap")
)

# Merge VWAP
df = df.merge(
    vwap_df,
    on="instrument_id",
    how="left"
)


# ----------------------------------
# Outlier Detection
# ----------------------------------

avg_price_df = (
    df.groupby("instrument_id")["price"]
    .mean()
    .reset_index(name="avg_price")
)

# Merge average price
df = df.merge(
    avg_price_df,
    on="instrument_id",
    how="left"
)

# Calculate deviation percentage
df["deviation_pct"] = (
    abs(df["price"] - df["avg_price"])
    / df["avg_price"]
)

# Flag outliers
df["is_outlier"] = (
    df["deviation_pct"] > 0.15
)


# ----------------------------------
# Final Clean Data
# ----------------------------------

final_df = df[[
    "instrument_id",
    "price",
    "volume",
    "timestamp",
    "vwap",
    "is_outlier"
]].copy()


# ----------------------------------
# Remove Microseconds
# ----------------------------------

final_df.loc[:, "timestamp"] = (
    pd.to_datetime(final_df["timestamp"])
    .dt.floor("s")
)


# ----------------------------------
# Remove Duplicate Records
# ----------------------------------

final_df = final_df.drop_duplicates(
    subset=["instrument_id", "timestamp"]
)


# ----------------------------------
# Load Into MySQL
# ----------------------------------

try:

    final_df.to_sql(
        name="market_data",
        con=engine,
        if_exists="append",
        index=False
    )

    logging.info(
        "Data loaded successfully into MySQL"
    )

except Exception as e:

    logging.error(
        f"Database Load Failed: {e}"
    )


# ----------------------------------
# Execution Metrics
# ----------------------------------

end_time = time.time()

execution_time = (
    end_time - start_time
)

logging.info(
    f"Records Processed: {len(final_df)}"
)

logging.info(
    f"Records Dropped: {dropped_records}"
)

logging.info(
    f"Execution Time: "
    f"{execution_time:.2f} seconds"
)


# ----------------------------------
# Final Data Preview
# ----------------------------------

print("\nFinal Processed Data:\n")

print(final_df)