from fastapi import FastAPI
from datetime import datetime
import random

app = FastAPI()

# Sample instruments
INSTRUMENTS = [
    "AAPL",
    "GOOG",
    "TSLA",
    "BTC-USD",
    "ETH-USD"
]

@app.get("/")
def home():
    return {
        "message": "Market Data API Running Successfully"
    }

@app.get("/v1/market-data")
def get_market_data():

    # Random fault probability
    fault_probability = random.random()

    # --------------------------------
    # Simulate API failure (2.5%)
    # --------------------------------

    if fault_probability < 0.025:

        return {
            "error": "Internal Server Error"
        }

    market_data = []

    # Generate 10 records
    for _ in range(10):

        record = {
            "instrument_id": random.choice(INSTRUMENTS),

            "price": round(
                random.uniform(100, 50000),
                2
            ),

            "volume": round(
                random.uniform(1, 1000),
                2
            ),

            "timestamp": datetime.utcnow().isoformat()
        }

        market_data.append(record)

    # --------------------------------
    # Simulate malformed data (2.5%)
    # --------------------------------

    if 0.025 <= fault_probability < 0.05:

        market_data[0]["price"] = "INVALID_PRICE"

    return market_data

    market_data = []

    # Generate 10 random records
    for _ in range(10):

        record = {
            "instrument_id": random.choice(INSTRUMENTS),

            "price": round(
                random.uniform(100, 50000),
                2
            ),

            "volume": round(
                random.uniform(1, 1000),
                2
            ),

            "timestamp": datetime.utcnow().isoformat()
        }

        market_data.append(record)

    return market_data