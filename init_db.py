# pylint: disable=missing-module-docstring
# pylint: disable=unused-variable

import io
from pathlib import Path
from streamlit.logger import get_logger

import duckdb
import pandas as pd

logger = get_logger(__name__)


def init_db(path_db_file: Path):
    """
    INITIALISE TABLES FOR SQL QUESTIONS
    memory_state : manage tables and contains info user
    :param path_db_file:
    :return:
    """
    dataframes = create_dataframes_for_exercises()

    with duckdb.connect(database=path_db_file, read_only=False) as con:
        for df_name, df in dataframes.items():
            logger.info("Creating table %s", df_name)
            con.execute(f"CREATE TABLE IF NOT EXISTS {df_name} AS SELECT * FROM df")


def create_dataframes_for_exercises():
    """

    :return:
    """
    dataframes = {}
    # ------------------------------------------------------------
    # EXERCISES LIST
    # ------------------------------------------------------------
    data = {
        "theme": ["cross_joins", "cross_joins"],
        "exercise_name": ["beverages_and_food", "sizes_and_trademarks"],
        "tables": [["beverages", "food_items"], ["sizes", "trademarks"]],
        "last_reviewed": ["1980-01-01", "1970-01-01"],
    }
    dataframes["memory_state"] = pd.DataFrame(data)
    # ------------------------------------------------------------
    # CROSS JOIN EXERCISES
    # ------------------------------------------------------------
    csv = """
    beverage,price
    orange juice,2.5
    Expresso,2
    Tea,3
    """
    dataframes["beverages"] = pd.read_csv(io.StringIO(csv))
    csv = """
    food_item,food_price
    cookie juice,2.5
    chocolatine,2
    muffin,3
    """
    dataframes["food_items"] = pd.read_csv(io.StringIO(csv))
    csv = """
    size
    XS
    M
    L
    XL
    """
    dataframes["sizes"] = pd.read_csv(io.StringIO(csv))
    csv = """
    trademark
    Nike
    Asphalte
    Abercrombie
    Lewis
    """
    dataframes["trademarks"] = pd.read_csv(io.StringIO(csv))
    return dataframes
