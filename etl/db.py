from sqlalchemy import create_engine

DATABASE_URL = (
    "mysql+pymysql://root:root@mysql:3306/market_db"
)

engine = create_engine(DATABASE_URL)