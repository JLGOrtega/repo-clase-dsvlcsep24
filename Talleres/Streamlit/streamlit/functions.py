import streamlit as st
import pandas as pd

def home(df):
    st.image("lobez.png", 
        caption="CARGATRON", width=400)
    
    with st.expander("Description:"):
        st.write("This is an app to visualise charging points.")
        st.dataframe(df)

def map(df):
    st.header("Mapa cargadores madrid")
    st.map(df, latitude="latidtud", longitude="longitud")

def charts(df):

    left, right = st.columns(2)

    with left:
                                     
        df_group_carg = df.groupby("DISTRITO")["Nº CARGADORES"].sum().reset_index()
        st.header("Cargadores por distrito")
        st.bar_chart(data = df_group_carg, 
                    x="DISTRITO", y="Nº CARGADORES")
    with right:
        st.header("Cargadores por Operador")
        df_group_oper = df.groupby("OPERADOR")[["Nº CARGADORES"]].sum().reset_index()
        st.bar_chart(data = df_group_oper, 
                    x="OPERADOR", y="Nº CARGADORES",)