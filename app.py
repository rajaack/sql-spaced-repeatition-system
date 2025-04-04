# pylint: disable=missing-module-docstring

from pathlib import Path

import duckdb
import pandas as pd
import streamlit as st
from streamlit.logger import get_logger

from init_db import init_db

st.text(
    """
SQL SRS
Spaced Repetition System SQL practice
"""
)


def check_user_query(user_query: str) -> None:
    """
    Check if user SQL query is correct by :
    1: check columns
    2: compare result with solution
    :param user_query: string containing the sql query
    """
    result = con.sql(user_query).df()
    try:
        result = result[solution_df.columns]
        result.compare(solution_df)
        st.markdown("**:green[Bonne réponse]**")
    except KeyError:
        st.error("Some columns are missing")
    n_lines_difference = result.shape[0] - solution_df.shape[0]
    if n_lines_difference != 0:
        st.error(
            f"result has a {n_lines_difference} lines difference with the solution_df"
        )
    st.dataframe(result)


def return_old_review_exercise_for_theme_selected() -> pd.DataFrame:
    """
    if user select a theme return the old reviewed exercise of the theme
    return the global old reviewed exercise if user doesn t select a theme
    :return: pd.Dataframe of memory_state
    """
    with st.sidebar:
        distinct_available_themes = (
            con.sql("SELECT DISTINCT theme FROM memory_state").df().values
        )
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

        return (
            con.sql(select_exercise_query)
            .df()
            .sort_values("last_reviewed")
            .reset_index()
        )


def return_the_answer_of_exercise_selected(exercise_name: str) -> str:
    """

    :param exercise_name:
    :return: the answer sql format from answers folder
    """
    with open(f"answers/{exercise_name}.sql", "r", encoding="utf-8") as f:
        return f.read()


logger = get_logger(__name__)

path_db_file = Path("data/exercises_sql_tables.duckdb")

init_db(path_db_file)

con = duckdb.connect(database=path_db_file, read_only=False)

exercise = return_old_review_exercise_for_theme_selected()

answer = return_the_answer_of_exercise_selected(exercise.loc[0, "exercise_name"])

solution_df = con.sql(answer).df()

st.header("enter your code:")
query = st.text_area(label="votre code SQL ici", key="user_input")

if query:
    check_user_query(query)

tab2, tab3 = st.tabs(["Tables", "Solution"])

with tab2:
    exercise_tables = exercise.loc[0, "tables"]
    for table in exercise_tables:
        st.write(f"table: {table}")
        df_table = con.sql(f"SELECT * FROM {table}").df()
        st.dataframe(df_table)

with tab3:
    st.text(answer)
