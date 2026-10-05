import os
from dotenv import load_dotenv
from sqlalchemy import create_engine

load_dotenv()
DB_PASSWORD = os.getenv("DB_PASSWORD")

engine = create_engine(
    f"postgresql+psycopg://postgres:{DB_PASSWORD}@localhost:5432/expense_tracker"
)