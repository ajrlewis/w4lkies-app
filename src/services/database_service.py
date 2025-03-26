import datetime

from loguru import logger
from sqlalchemy.sql import text

from app import db

tables = ["user", "customer", "vet", "dog", "service", "booking", "expense", "invoice"]


def wake_up_database(max_attempts=5, initial_delay=1, max_delay=30):
    delay = initial_delay
    for attempt in range(max_attempts):
        try:
            db.session.execute(text("SELECT 1"))
            return True
        except Exception as e:
            if attempt < max_attempts - 1:
                time.sleep(delay)
                delay = min(delay * 2, max_delay)  # exponential backoff
            else:
                raise Exception(
                    f"Failed to wake up database after {max_attempts} attempts: {str(e)}"
                )


def dump_database():
    list_of_table_data = []
    for table in tables:
        table_data = {f"{table}": "", "data": []}
    return


def load_database():
    pass
