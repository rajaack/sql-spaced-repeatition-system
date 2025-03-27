import streamlit as st
import pandas as pd
import duckdb

data = {"a": [1,2,3], "b": [4,5,6]}

df = pd.DataFrame(data)

st.write("Dataframe initial :")
st.dataframe(df)
query = st.text_area(label="entrez votre input")

if query:
    st.write(duckdb.sql(query).df())
