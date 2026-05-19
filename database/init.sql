CREATE DATABASE IF NOT EXISTS market_db;

USE market_db;

CREATE TABLE IF NOT EXISTS market_data (

    id INT AUTO_INCREMENT PRIMARY KEY,

    instrument_id VARCHAR(50) NOT NULL,

    price FLOAT NOT NULL,

    volume FLOAT NOT NULL,

    timestamp DATETIME NOT NULL,

    vwap FLOAT,

    is_outlier BOOLEAN,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    UNIQUE KEY unique_market_record (
        instrument_id,
        timestamp
    )
);