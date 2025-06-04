import streamlit as st
import pandas as pd
import requests
import json


df = pd.read_csv("Data/info_film_leger.csv")
df_film = df[df['tconst'] == "tt0117060"]


url_imdb_id = "https://api.themoviedb.org/3/find/tt0117060?external_source=imdb_id"

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

    liste_director = []

    for idx in range(df_film.loc[(df_film['category'] == "director"), "primaryName"].shape[0]):
        liste_director.append(df_film.loc[(df_film['category'] == "director"), "primaryName"].iloc[idx])

    st.write("Director : " + ", ".join(liste_director))

######################### Récupération des acteurs du film ########################

    liste_actors = []

    for idx in range(df_film.loc[(df_film['category'] == "actor") | (df_film['category'] == "actress"), "primaryName"].shape[0]):
         
        liste_actors.append(df_film.loc[(df_film['category'] == "actor") | (df_film['category'] == "actress"), "primaryName"].iloc[idx])

   

########################## Affichage non des acteurs et images associés ##########

    st.write("Actors : ")

    img1, img2, img3 = st.columns(3)

    liste_image_acteur = []
    for idx in range(len(credits["cast"][:3])):
        liste_image_acteur.append(credits["cast"][idx]["profile_path"])

    with img1:

        st.write(liste_actors[0])
        st.image("https://image.tmdb.org/t/p/original/" + liste_image_acteur[0])

    with img2:
        st.write(liste_actors[1])
        st.image("https://image.tmdb.org/t/p/original/" + liste_image_acteur[1])

    with img3:
        st.write(liste_actors[2])
        st.image("https://image.tmdb.org/t/p/original/" + liste_image_acteur[2])