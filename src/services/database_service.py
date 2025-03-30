import datetime
import json

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


# Convert datetime values to strings
def convert_json_datetime(obj):
    try:
        return obj.isoformat()
    except AttributeError:
        try:
            return str(obj)
        except Exception as e:
            raise TypeError(f"Unknown type: {type(obj)}") from e


def dump_database() -> str:
    """
    Dump the data from the specified tables in the database.

    Returns:
        dict: A dictionary with table names as keys and lists of rows as values.
    """
    table_data = {}
    for table_name in tables:
        table_obj = db.metadata.tables.get(table_name)
        if table_obj is None:
            logger.error(f"Table {table_name} not found in database")
            continue

        columns = [column.name for column in table_obj.columns]
        table_rows_data = [
            dict(zip(columns, row)) for row in db.session.query(table_obj).all()
        ]
        table_data[table_name] = table_rows_data

    logger.debug(f"Dumped data: {table_data}")

    dumped_json = json.dumps(table_data, default=convert_json_datetime, indent=4)
    logger.debug(f"Dumped data: {dumped_json}")
    return dumped_json


import importlib

table_names = [
    "user",
    "customer",
    "vet",
    "dog",
    "service",
    "invoice",
    "booking",
    "expense",
]
table_names = ["expense"]


def load_database(table_data: dict):
    for table_name, table_rows in table_data.items():
        if table_name not in table_names:
            continue

        table_obj = db.metadata.tables.get(table_name)
        if table_obj is None:
            logger.error(f"Table {table_name} not found in database metadata")
            continue

        module_name = f"{table_name}_service"
        service_module = importlib.import_module(f"services.{module_name}")
        print(f"{service_module = }")

        for table_row in table_rows:
            logger.debug(f"Adding {table_row = }")
            method_name = f"add_{table_name}"
            method = getattr(service_module, method_name)
            method(table_row)
