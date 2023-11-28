import streamlit as st
import pandas as pd

df = pd.read_csv("top30_current.csv")
st.title("전국 인기 사업장 30개")

pivot_table = pd.pivot_table(df, index="업종", values=['당월'])
