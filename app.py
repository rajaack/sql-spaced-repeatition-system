# pylint: disable=missing-module-docstring

import ast

import duckdb
import streamlit as st

st.write(
    """
SQL SRS
Spaced Repetition System SQL practice
"""
)

con = duckdb.connect(database="data/exercises_sql_tables.duckdb", read_only=False)

# solution_df = duckdb.sql(ANSWER_STR).df()

with st.sidebar:
    theme = st.selectbox(
        "What would you like to review?",
        ("cross_joins", "GroupBy", "window_functions"),
        index=None,
        placeholder="Select a theme ...",
    )

    exercise = con.execute(f"SELECT * FROM memory_state WHERE theme = '{theme}'").df()
    st.write(exercise)

data = {"a": [1, 2, 3], "b": [4, 5, 6]}

st.header("enter your code:")
query = st.text_area(label="votre code SQL ici", key="user_input")
if query:
    result = con.execute(query).df()
    st.dataframe(result)

    # try:
    #     result = result[solution_df.columns]
    #     result.compare(solution_df)
    #     st.markdown("**:green[Bonne réponse]**")
    # except KeyError:
    #     st.error("Some columns are missing!")

tab2, tab3 = st.tabs(["Tables", "Solution"])

with tab2:
    exercise_tables = ast.literal_eval(exercise.loc[0, "tables"])
    for table in exercise_tables:
        st.write(f"table: {table}")
        df_table = con.execute(f"SELECT * FROM {table}").df()
        st.dataframe(df_table)

with tab3:
    exercise_name = exercise.loc[0, "exercise_name"]
    with open(f"answers/{exercise_name}.sql", "r", encoding="utf-8") as f:
        answer = f.read()
    st.write(answer)
