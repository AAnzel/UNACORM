import datetime

import pandas as pd
import streamlit as st
import text_content as tc
import utilities as uti

df_existing_detail = pd.read_pickle(uti.PATH_EXISTING_DETAIL)

with st.container(
    border=False,
    horizontal=True,
    horizontal_alignment="center",
    gap="small",
):
    st.info(tc.STRING_INTRODUCTION, width=1300)

st.space(size="medium")


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
float_success_rate = (
    df_existing_detail[df_existing_detail["Transformation"] == "Decoding"][
        "Similarity"
    ].mean()
    * 100
)

str_success_rate = str(f"{float_success_rate:.2f} %")

with st.container(
    border=False,
    horizontal=True,
    horizontal_alignment="center",
    gap="large",
):
    st.metric(
        ":primary[:material/genetics:]$~~~~$Coding Schemes (Codecs)",
        int_sum_methods,
        border=True,
        width=300,
    )
    st.metric(
        ":primary[:material/files:]$~~~~$Files Encoded",
        int_sum_files,
        border=True,
        width=300,
    )
    st.metric(
        ":primary[:material/storage:]$~~~~$Encoded and Decoded in Total",
        str_sum_size,
        border=True,
        width=300,
    )

st.space(size="medium")

with st.container(
    border=False,
    horizontal=True,
    horizontal_alignment="center",
    gap="large",
):
    st.metric(
        ":primary[:material/timer:]$~~~~$Encoding and Decoding Lasted",
        str_sum_time,
        border=True,
        width=300,
    )
    st.metric(
        ":primary[:material/attach_money:]$~~~~$Sum of Costs in US Dollars",
        str_sum_cost,
        border=True,
        width=300,
    )
    st.metric(
        ":primary[:material/check_circle:]$~~~~$Succesfully Encoded and Decoded",
        str_success_rate,
        border=True,
        width=300,
    )

uti.display_footer()
