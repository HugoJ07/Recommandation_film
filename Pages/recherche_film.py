import streamlit as st
import pandas as pd
import requests
import json

def show():
    headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIzZGJlNWFjZDc1YmIzMWVlYTE2ZmMyY2VkMjU5YmM5ZiIsIm5iZiI6MTc0ODg1OTEyMy41MDQsInN1YiI6IjY4M2Q3OGYzMzVmOGU1MjAxODUzODM2YiIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.06eO4o3IsGnUgXiyrinBOs0jUrexp-CLvKUjbJruAJY"
    }
    st.title("Application de recommendation de film")

    df_machin = pd.read_csv("Data/title_sup_1950.csv")

    selected = st.selectbox("Que voulez vous rechercher ?", ['Film', 'Acteur', 'Réalisateur'])

    if selected == "Film":
        search = st.text_input("Search movies by title", value="").lower()
        titre = df_machin["originalTitle"].str.lower().str.contains(search)
        df_title = df_machin[titre].reset_index()

        if search:
            liste_id_imdb = df_title['tconst'].to_list()

            liste_poster_recherche = []
            liste_id_film = []
            for id in liste_id_imdb:
                url = "https://api.themoviedb.org/3/find/"+ id +"?external_source=imdb_id"
                response = requests.get(url, headers=headers)
                data = json.loads(response.text)

                try:
                    liste_poster_recherche.append("https://image.tmdb.org/t/p/w500/" + data["movie_results"][0]["poster_path"])
                    liste_id_film.append(id)  # Je conserve les Id qui ont marché
                except:
                    continue

            cols = st.columns(4)

            for idx, (image, film_id) in enumerate(zip(liste_poster_recherche[:40], liste_id_film[:40])):
                col = cols[idx % 4]
                col.image(image, use_container_width=True)
                if col.button("Voir les détails", key=f"detail_{idx}"):
                    st.session_state['selected_film'] = film_id
                    st.session_state['page'] = 'test'
                    st.rerun()
