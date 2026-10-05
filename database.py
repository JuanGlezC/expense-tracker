import os
from dotenv import load_dotenv
from sqlalchemy import create_engine

load_dotenv()
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST", "localhost")

engine = create_engine(
    f"postgresql+psycopg://postgres:{DB_PASSWORD}@{DB_HOST}:5432/expense_tracker"
)