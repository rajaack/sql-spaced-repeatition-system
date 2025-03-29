import streamlit as st
import pandas as pd
import duckdb

st.write("""
SQL SRS
Spaced Repetition System SQL practice
""")

with st.sidebar:
    option = st.selectbox(
        "What would you like to review?",
        ("Joins", "GroupBy", "Windows Functions"),
        index=None,
        placeholder="Select a theme ...",
    )

    st.write(f"You selected : {option}")

data = {"a": [1,2,3], "b": [4,5,6]}

df = pd.DataFrame(data)

st.write("Dataframe initial :")
st.dataframe(df)
query = st.text_area(label="entrez votre input")

if query:
    st.write(duckdb.sql(query).df())
