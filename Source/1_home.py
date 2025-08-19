import datetime

import pandas as pd
import streamlit as st
import text_content as tc
import utilities as uti

df_existing_detail = pd.read_pickle(uti.PATH_EXISTING_DETAIL)

_, st_col_2, _ = st.columns([1, 9, 1])
with st_col_2:
    st.info(tc.STRING_INTRODUCTION)
    st.html("<br><br>")


str_sum_time = str(
    datetime.timedelta(seconds=df_existing_detail["Time"].sum())
).split(".")[0]
str_sum_cost = str(
    "{:.2f} M".format(df_existing_detail["Cost"].sum() / 1000000)
)
str_sum_size = str(
    "{:.2f} MB".format(df_existing_detail["Size"].sum() / 8000000)
)
int_sum_methods = len(uti.LIST_ENCODING_METHODS)
int_sum_files = len(list(pd.unique(df_existing_detail["Filename"])))
series_success_rate = df_existing_detail["Similarity"].value_counts(  # pyright: ignore [reportAttributeAccessIssue]
    normalize=True
)

str_success_rate = str("{:.2f} %".format(series_success_rate[True]))

_, st_col_1, st_col_2, st_col_3, _ = st.columns([1, 3, 3, 3, 1])
_, st_col_4, st_col_5, st_col_6, _ = st.columns([1, 3, 3, 3, 1])

st_col_1.metric(
    ":primary[:material/genetics:]$~~~~$Encoding Methods",
    int_sum_methods,
    border=True,
)
st_col_2.metric(
    ":primary[:material/files:]$~~~~$Files Encoded", int_sum_files, border=True
)
st_col_3.metric(
    ":primary[:material/storage:]$~~~~$Encoded and Decoded in Total",
    str_sum_size,
    border=True,
)
st_col_4.metric(
    ":primary[:material/timer:]$~~~~$Encoding and Decoding Lasted",
    str_sum_time,
    border=True,
)
st_col_5.metric(
    ":primary[:material/attach_money:]$~~~~$Sum of Costs in US Dollars",
    str_sum_cost,
    border=True,
)
st_col_6.metric(
    ":primary[:material/check_circle:]$~~~~$Succesfully Encoded and Decoded",
    str_success_rate,
    border=True,
)

uti.display_footer()
