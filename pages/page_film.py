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
st.markdown(
"""
<style>
    [data-testid="stMainBlockContainer"] {max-width: 1000px;}
    [data-testid="stSidebar"] {display: none;}
    [data-testid="stColumn"] {padding:0;}
    [data-testid="stImage"] img {
        width: 100%;
        height: 100%;
        display: block;}
    [data-testid="stHorizontalBlock"] img {
    [data-testid="stMarkdownContainer"] p {margin:2px}
    }
    [data-testid="stColumn"] {
        background:rgba(19, 23, 32,0.8);
        height: 100%;
    }
    [data-testid="stVerticalBlock"] {
        text-align: center;
    }
    .stApp{
        background-image: url("https://www.boxofficepro.fr/wp-content/uploads/sites/2/2020/12/salle-N%C2%B03-Atalante-1-%C2%A9-Mathieu-Prat-copie.jpg");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
    }
</style>
""", 
unsafe_allow_html=True)


df = pd.read_csv("Data/donnees_model_reco_V2.csv")

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
if st.button("Accueil", key="accueil_btn"):    
    st.switch_page("app.py")
st.header(details_fr['title'])

col1, col2 = st.columns([2,2], border=True)

with col1:
    
    st.image("https://image.tmdb.org/t/p/original/" + details_fr['poster_path'])


with col2:

    st.write("**Date de sortie**: " + details_fr['release_date'])
    list_genre= []
    for idx in range(len(details_fr["genres"])):
        list_genre.append(details_fr["genres"][idx]["name"])
    genres = ', '.join(list_genre)
    st.write("**Genre** : " + genres)

    note = round(details_fr['vote_average'],2)
    st.write("**Note** : " + str(note) + "/10")

    st.write(details_fr['overview'])


########################## Récupération du/des réalisateurs du film ##################
    for idx in range(len(credits['crew'])):
        if credits['crew'][idx]['known_for_department'] == 'Directing':
            director = credits['crew'][idx]['name']
            break

    try:   
        st.write("**Réalisateur** : " + director)
    except:
        st.write("**Réalisateur** : ")

########################## Affichage non des acteurs et images associés ##########

    st.write("**Acteurs** : ")

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
    st.write("**Bande annonce** :")
    st.video(url_youtube+short_url)
except:
    try:
        short_url = video_en['results'][0]['key']
        url_youtube = "https://www.youtube.com/watch?v="
        st.write("**Bande annonce** :")
        st.video(url_youtube+short_url)
    except:
        pass

st.divider()

###################### Film de la même saga #####################

if details_fr["belongs_to_collection"]:
    
    id_collection = details_fr["belongs_to_collection"]["id"]

    url_collection = "https://api.themoviedb.org/3/collection/" + str(id_collection) + "?language=fr-FR"
    response_id_collection = requests.get(url_collection, headers=headers)
    collection = json.loads(response_id_collection.text)

    st.write("**Découvrez les films de la même collection :**")

    colonne_saga = st.columns(4)

    liste_id_saga = []

    for idx in range(len(collection["parts"])):

        tmdb_id_saga = collection["parts"][idx]["id"]
        

        url_imdb_from_tmdb = "https://api.themoviedb.org/3/movie/" + str(tmdb_id_saga) + "/external_ids"
        response_imdb_from_tmdb = requests.get(url_imdb_from_tmdb, headers=headers)
        imdbid = json.loads(response_imdb_from_tmdb.text)

        imdb_id_from_tmdb = imdbid['imdb_id']

        liste_id_saga.append(imdb_id_from_tmdb)

        try:
            with colonne_saga[idx%4]:

                url_img_saga = "https://image.tmdb.org/t/p/w500/" + collection["parts"][idx]["poster_path"]

                st.image(url_img_saga)
                
                if st.button("Cliquer ici pour plus d'informations", key=tmdb_id_saga):
                            st.session_state['selected_film'] = imdb_id_from_tmdb
                            st.session_state["bouton_reco"] = False
                            st.switch_page("pages/page_film.py")
        except:
            pass

    st.divider()
else : 
    liste_id_saga = []

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

    count = 0
    for idx, (id_imdb_reco, poster) in enumerate(dic_poster.items()):
        if id_imdb_reco not in liste_id_saga:
            if poster is not None:
                if count < 5:
                    
                    with cols[count]:
                        count += 1 

                        url_img = "https://image.tmdb.org/t/p/w500/" + poster
                        st.markdown(
                                f'''
                                <img src="{url_img}" style="height:250px; width:100%; display:block; margin-left:auto; margin-right:auto; border-radius: 8px; margin-bottom : 15px;" />
                                ''',
                                    unsafe_allow_html=True)
                        
                        if st.button("Cliquer ici pour plus d'informations", key=id_imdb_reco):
                            st.session_state['selected_film'] = id_imdb_reco
                            st.session_state["bouton_reco"] = False
                            st.switch_page("pages/page_film.py")