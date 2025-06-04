import streamlit as st
import pandas as pd


st.title("Application de recommendation de film")


df_machin = pd.read_csv("title_sup_1950.csv")


st.write(df_machin)

selected = st.selectbox("Que voulez vous rechercher ?",

             ['Film', 'Acteur', 'Réalisateur']) 

if selected == "Film":
    search = st.text_input("Search movies by title", value="")
    titre = df_machin["originalTitle"].str.contains(search)
    df_title = df_machin[titre].reset_index()
    
    if search:
        st.write(df_title["originalTitle"])

elif selected == "Acteur": 
    search = st.text_input("Search movies by actor", value="")

else: 
    search = st.text_input("Seach movies by realisateur",value="")

