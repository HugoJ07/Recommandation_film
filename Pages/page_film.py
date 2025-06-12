import streamlit as st
import pandas as pd
import requests
import json

st.set_page_config(initial_sidebar_state="collapsed")

df = pd.read_csv("Data/info_film_leger.csv")

imdb_id = st.session_state['selected_film']

df_film = df[df['tconst'] == imdb_id]


url_imdb_id = "https://api.themoviedb.org/3/find/"+ imdb_id+ "?external_source=imdb_id"

headers = {
    "accept": "application/json",
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIzZGJlNWFjZDc1YmIzMWVlYTE2ZmMyY2VkMjU5YmM5ZiIsIm5iZiI6MTc0ODg1OTEyMy41MDQsInN1YiI6IjY4M2Q3OGYzMzVmOGU1MjAxODUzODM2YiIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.06eO4o3IsGnUgXiyrinBOs0jUrexp-CLvKUjbJruAJY"
}

response_imdb_id = requests.get(url_imdb_id, headers=headers)
info_film = json.loads(response_imdb_id.text)

tmdb_id = info_film["movie_results"][0]["id"]

url_credits = "https://api.themoviedb.org/3/movie/" + str(tmdb_id) + "/credits"
response_credits = requests.get(url_credits, headers=headers)
credits = json.loads(response_credits.text)


##########################################################################

st.header(info_film["movie_results"][0]["title"])

col1, col2 = st.columns(2)

with col1:
    st.image("https://image.tmdb.org/t/p/w500/" + info_film["movie_results"][0]["poster_path"])


with col2:
    st.write(info_film["movie_results"][0]["overview"])

    #st.write("Release date : " + (df_film["startYear"].iloc[0].astype(str)))

########################## Récupération du/des réalisateurs du film
    
    liste_director = df_film.loc[(df_film['category'] == "director"), "primaryName"].to_list()

    st.write("Director : " + ", ".join(liste_director))


########################## Affichage non des acteurs et images associés ##########

    st.write("Actors : ")

    img = st.columns(3)

    for idx in range(3):
        with img[idx]:
            st.write(credits["cast"][idx]["name"])
            if credits["cast"][idx]["profile_path"]:  
                st.image("https://image.tmdb.org/t/p/original/" + credits["cast"][idx]["profile_path"])
