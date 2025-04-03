"""
INITIALISE TABLES FOR SQL QUESTIONS
memory_state : manage tables and contains info user
"""

import io
from pathlib import Path

import duckdb
import pandas as pd

PATH_DB_FILE = "data/exercises_sql_tables.duckdb"

# delete DB if exists
Path(PATH_DB_FILE).unlink(missing_ok=True)

# create new DB
con = duckdb.connect(database=PATH_DB_FILE, read_only=False)

# ------------------------------------------------------------
# EXERCISES LIST
# ------------------------------------------------------------
data = {
    "theme": ["cross_joins", "cross_joins2", "window_functions"],
    "exercise_name": ["beverages_and_food", "size_and_trademark", "simple_window"],
    "tables": [["beverages", "food_items"], ["size", "trademark"], "simple_window"],
    "last_reviewed": ["1970-01-01", "1970-01-01", "1970-01-01"],
}
memory_state_df = pd.DataFrame(data)
con.execute("CREATE TABLE IF NOT EXISTS memory_state AS SELECT * FROM memory_state_df")

# ------------------------------------------------------------
# CROSS JOIN EXERCISES
# ------------------------------------------------------------
CSV = """
beverage,price
orange juice,2.5
Expresso,2
Tea,3
"""
beverages = pd.read_csv(io.StringIO(CSV))
con.execute("CREATE TABLE IF NOT EXISTS beverages AS SELECT * FROM beverages")

CSV2 = """
food_item,food_price
cookie juice,2.5
chocolatine,2
muffin,3
"""
food_items = pd.read_csv(io.StringIO(CSV2))
con.execute("CREATE TABLE IF NOT EXISTS food_items AS SELECT * FROM food_items")

CSV3 = """
size
XS
M
L
XL
"""
size = pd.read_csv(io.StringIO(CSV3))
con.execute("CREATE TABLE IF NOT EXISTS size AS SELECT * FROM size")

CSV4 = """
trademark
Nike
Asphalte
Abercrombie
Lewis
"""
trademark = pd.read_csv(io.StringIO(CSV4))
con.execute("CREATE TABLE IF NOT EXISTS trademark AS SELECT * FROM trademark")
