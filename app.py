# pylint: disable=missing-module-docstring

from pathlib import Path

import duckdb
import streamlit as st
from streamlit.logger import get_logger
from init_db import init_db

st.text(
    """
SQL SRS
Spaced Repetition System SQL practice
"""
)

logger = get_logger(__name__)

path_db_file = Path("data/exercises_sql_tables.duckdb")

if not path_db_file.parent.exists():
    logger.info("creating folder %s", path_db_file.parent)
    path_db_file.parent.mkdir(parents=True)

if not path_db_file.exists():
    logger.info("creation a new database")
    init_db(path_db_file)

con = duckdb.connect(database=path_db_file, read_only=True)

with st.sidebar:
    distinct_available_themes = con.sql("SELECT DISTINCT theme FROM memory_state").df().values
    theme = st.selectbox(
        "What would you like to review?",
        distinct_available_themes,
        index=None,
        placeholder="Select a theme ...",
    )

    select_exercise_query = "SELECT * FROM memory_state"
    if theme:
        st.write(f"You selected {theme}")
        select_exercise_query += f" WHERE theme = '{theme}'"

    exercise = (
        con.sql(select_exercise_query)
        .df()
        .sort_values("last_reviewed")
        .reset_index()
    )
    st.write(exercise)

exercise_name = exercise.loc[0, "exercise_name"]
with open(f"answers/{exercise_name}.sql", "r", encoding="utf-8") as f:
    answer = f.read()

solution_df = con.sql(answer).df()

data = {"a": [1, 2, 3], "b": [4, 5, 6]}

st.header("enter your code:")
query = st.text_area(label="votre code SQL ici", key="user_input")
if query:
    result = con.sql(query).df()

    try:
        result = result[solution_df.columns]
        result.compare(solution_df)
        st.markdown("**:green[Bonne réponse]**")
    except KeyError as e:
        st.error("Some columns are missing")

    n_lines_difference = result.shape[0] - solution_df.shape[0]
    if n_lines_difference != 0:
        st.error(
            f"result has a {n_lines_difference} lines difference with the solution_df"
        )

    st.dataframe(result)

tab2, tab3 = st.tabs(["Tables", "Solution"])

with tab2:
    exercise_tables = exercise.loc[0, "tables"]
    for table in exercise_tables:
        st.write(f"table: {table}")
        df_table = con.sql(f"SELECT * FROM {table}").df()
        st.dataframe(df_table)

with tab3:
    st.text(answer)
