import streamlit as st
import pandas as pd
import requests
import json
headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIzZGJlNWFjZDc1YmIzMWVlYTE2ZmMyY2VkMjU5YmM5ZiIsIm5iZiI6MTc0ODg1OTEyMy41MDQsInN1YiI6IjY4M2Q3OGYzMzVmOGU1MjAxODUzODM2YiIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.06eO4o3IsGnUgXiyrinBOs0jUrexp-CLvKUjbJruAJY"
        }
st.title("Application de recommendation de film")


df_machin = pd.read_csv("Data/title_sup_1950.csv")

#st.write(df_machin)

selected = st.selectbox("Que voulez vous rechercher ?", ['Film', 'Acteur', 'Réalisateur'])

if selected == "Film":
    search = st.text_input("Search movies by title", value="")
    titre = df_machin["originalTitle"].str.contains(search)
    df_title = df_machin[titre].reset_index()
    
    if search:

        liste_id_imdb = df_title['tconst'].to_list()

        liste_poster_recherche = []
        for id in liste_id_imdb:
        
            url = "https://api.themoviedb.org/3/find/"+ id +"?external_source=imdb_id"

            response = requests.get(url, headers=headers)

            data = json.loads(response.text)

            try:
                liste_poster_recherche.append("https://image.tmdb.org/t/p/w500/" + data["movie_results"][0]["poster_path"])
            except:
                None

        
        st.image(liste_poster_recherche[:10])

# elif selected == "Acteur": 
#     search = st.text_input("Search movies by actor", value="")

# else: 
#     search = st.text_input("Seach movies by realisateur",value="")
