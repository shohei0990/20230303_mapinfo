import streamlit as st
import pandas as pd

# セッションステートを取得
state = st.session_state

if "name" not in state:
    state.name = "Streamlit"
if "df" not in state:
    state.df = pd.DataFrame()

st.write("Page A")

st.write(f"Hello, {state.name}!")

se90 = st.write(state.df)
se91 = st.write(state.df.shape)
