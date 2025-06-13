import streamlit as st
import pandas as pd
import requests
import json
import pickle


if "selected_film" not in st.session_state:
    st.warning("Aucun film sélectionné. Veuillez revenir à la page d’accueil.")
    st.stop()

imdb_id = st.session_state['selected_film']

st.set_page_config(initial_sidebar_state="collapsed")

df = pd.read_csv("Data/donnees_model_reco.csv")

df_film = df[df['tconst'] == imdb_id]

###################### Récupération des infos via l'API TMDB #############################

headers = {
    "accept": "application/json",
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIzZGJlNWFjZDc1YmIzMWVlYTE2ZmMyY2VkMjU5YmM5ZiIsIm5iZiI6MTc0ODg1OTEyMy41MDQsInN1YiI6IjY4M2Q3OGYzMzVmOGU1MjAxODUzODM2YiIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.06eO4o3IsGnUgXiyrinBOs0jUrexp-CLvKUjbJruAJY"
}

url_imdb_id = "https://api.themoviedb.org/3/find/"+ imdb_id+ "?external_source=imdb_id"

response_imdb_id = requests.get(url_imdb_id, headers=headers)
info_film = json.loads(response_imdb_id.text)
tmdb_id = info_film["movie_results"][0]["id"]

url_details_fr = "https://api.themoviedb.org/3/movie/"+ str(tmdb_id) +"?language=fr-FR"
response_details_fr = requests.get(url_details_fr, headers=headers)
details_fr = json.loads(response_details_fr.text)

url_credits = "https://api.themoviedb.org/3/movie/" + str(tmdb_id) + "/credits"
response_credits = requests.get(url_credits, headers=headers)
credits = json.loads(response_credits.text)

url_video = "https://api.themoviedb.org/3/movie/"+str(tmdb_id)+"/videos?language=fr-FR"
response_video = response_credits = requests.get(url_video, headers=headers)
video = json.loads(response_video.text)

url_video_en = "https://api.themoviedb.org/3/movie/"+str(tmdb_id)+"/videos"
response_video_en = response_credits = requests.get(url_video_en, headers=headers)
video_en = json.loads(response_video_en.text)

# Chargement des données, du modèle et du preprocessor pour le ML

with open("Data/preprocessor.pkl", 'rb') as file_preprocessor:
    preprocessor = pickle.load(file_preprocessor)


with open("Data/model_knn.pkl", 'rb') as file_model:
    model_knn = pickle.load(file_model)


with open("Data/donnees_clean_ml.pkl", 'rb') as file_donnees_model:
    X = pickle.load(file_donnees_model)


##################################################################################

st.header(details_fr['title'])

col1, col2 = st.columns([2,2], border=True)

with col1:
    st.image("https://image.tmdb.org/t/p/original/" + details_fr['poster_path'])


with col2:

    st.write("Date de sortie : " + details_fr['release_date'])

    note = round(details_fr['vote_average'],2)
    st.write("Note : " + str(note) + "/10")

    st.write(details_fr['overview'])


########################## Récupération du/des réalisateurs du film ##################
    for idx in range(len(credits['crew'])):
        if credits['crew'][idx]['known_for_department'] == 'Directing':
            director = credits['crew'][idx]['name']
            break

    try:   
        st.write("Réalisateur : " + director)
    except:
        st.write("Réalisateur : ")

########################## Affichage non des acteurs et images associés ##########

    st.write("Acteurs : ")

    img = st.columns(3)
    for idx in range(3):
        with img[idx]:
            try:
                st.write(credits["cast"][idx]["name"])
                if credits["cast"][idx]["profile_path"]:  
                    st.image("https://image.tmdb.org/t/p/original/" + credits["cast"][idx]["profile_path"])
            except:
                pass


st.divider()

try :
    short_url = video['results'][0]['key']
    url_youtube = "https://www.youtube.com/watch?v="
    st.write("Bande annonce :")
    st.video(url_youtube+short_url)
except:
    try:
        short_url = video_en['results'][0]['key']
        url_youtube = "https://www.youtube.com/watch?v="
        st.write("Bande annonce :")
        st.video(url_youtube+short_url)
    except:
        pass


##################### RECOMMENDATION ############################

if "bouton_reco" not in st.session_state:
    st.session_state["bouton_reco"] = False

if st.button(f"Découvrez nos recommandations si " + details_fr['title'] + " vous a plu !", use_container_width=True):
    st.session_state['bouton_reco'] = True

if st.session_state['bouton_reco']:

    index_cible = df_film.index
    
    cible_transformed = preprocessor.transform(X.loc[index_cible])
    distance, indice = model_knn.kneighbors(cible_transformed)

    id_voisins = df.iloc[indice[0]]['tconst'].to_list()

    dic_poster = {}
    for idx, id in enumerate(id_voisins):
        if idx >= 1:     
            url = "https://api.themoviedb.org/3/find/"+ id +"?external_source=imdb_id&language=fr-FR"

            response = requests.get(url, headers=headers)

            data = json.loads(response.text)

            try:
                dic_poster[id] = data["movie_results"][0]["poster_path"]
            except:
                pass

    cols = st.columns(5)

    for idx, (id_imdb_reco, poster) in enumerate(dic_poster.items()):
        if poster is not None: 
            with cols[idx]:
                st.image("https://image.tmdb.org/t/p/w500/" + poster)
                if st.button("Cliquer ici pour plus d'informations", key=id_imdb_reco):
                    st.session_state['selected_film'] = id_imdb_reco
                    st.session_state["bouton_reco"] = False
                    st.switch_page("pages/page_film.py")