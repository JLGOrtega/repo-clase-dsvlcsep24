import pandas as pd
import matplotlib.pyplot as plt 
import streamlit as st
from functions import home, map, charts


# LO DE FUERA

st.set_page_config(
    page_title="Cargatron",
    page_icon=":rocket:",
    layout="wide",
    initial_sidebar_state="expanded",
)

# A PARTIR DE AQUI LAS PAGINAS 
option = st.sidebar.selectbox(
    "Page:",
    ("Home", "Map", "Charts"),
)


st.header(f"My Streamlit APP - CARGATRON")


df = pd.read_csv("data/red_recarga_acceso_publico_2021.csv", sep=";")

uploaded_file = st.sidebar.file_uploader("Choose a file (must be ';' separated)", 
                                 type=["csv"]

                                 )
if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file, sep=";")
        st.balloons()
    except:
        st.write("File format not recognized.")

filtro_D = st.sidebar.multiselect(
    "Distrito:",
    df.DISTRITO.unique().tolist(),
    df.DISTRITO.unique().tolist(),
)

df = df.loc[ df["DISTRITO"].isin(filtro_D)    ,  :]




# filtro_D = st.sidebar.selectbox(
#     "Distrito:",
#     df.DISTRITO.unique().tolist(),
    
# )

# if filtro_D == "ALL":
#     pass
# else:
#     df = df.loc[ df["DISTRITO"].isin([filtro_D])    ,  :]





# st.write("You selected:", option)
if option == "Home":
    home(df)
elif option=="Map":
    map(df)
else: 
    charts(df)

