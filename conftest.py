import os

import pytest
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

from api import app, get_gestor
from gestor import GestorGastos
from GastoORM import Base

load_dotenv()
DB_PASSWORD = os.getenv("DB_PASSWORD")


@pytest.fixture(scope="session")
def engine_test():
    engine = create_engine(
        f"postgresql+psycopg://postgres:{DB_PASSWORD}@localhost:5432/expense_tracker_test"
    )
    Base.metadata.create_all(engine)
    yield engine
    engine.dispose()


@pytest.fixture(autouse=True)
def bd_limpia(engine_test):
    with engine_test.begin() as conexion:
        conexion.execute(text("TRUNCATE TABLE gastos"))
    app.dependency_overrides[get_gestor] = lambda: GestorGastos(engine_test)
    yield
    app.dependency_overrides.clear()