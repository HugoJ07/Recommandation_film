import streamlit as st
import pandas as pd
import requests
import json
import re

st.set_page_config(initial_sidebar_state="collapsed")


headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIzZGJlNWFjZDc1YmIzMWVlYTE2ZmMyY2VkMjU5YmM5ZiIsIm5iZiI6MTc0ODg1OTEyMy41MDQsInN1YiI6IjY4M2Q3OGYzMzVmOGU1MjAxODUzODM2YiIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.06eO4o3IsGnUgXiyrinBOs0jUrexp-CLvKUjbJruAJY"
    }
st.title("Application de recommendation de film")

df_title = pd.read_csv("Data/title_sup_1950.csv")
df_title = df_title[["tconst", 'originalTitle', 'title', 'startYear']]
df_info = pd.read_csv("Data/info_film_leger.csv")
df_info = df_info[['tconst', 'primaryName', 'category']]


df_title["title"] = df_title["title"].str.replace(r"[^\w]", "", regex=True)
df_title["originalTitle"] = df_title["originalTitle"].str.replace(r"[^\w]", "", regex=True)


selected = st.selectbox("Que voulez vous rechercher ?", ['Film', 'Acteur', 'Réalisateur'])

if selected == "Film":
    try :
     
        search = st.text_input("Rechercher par titre de film", value="").lower()
        search = re.sub(r"[^\w]", "", search)
        titre_exact = (df_title["title"].str.lower() == search) | (df_title["originalTitle"].str.lower() == search)
        titre_partielle = (df_title["title"].str.lower().str.contains(search, na=False)) | (df_title["originalTitle"].str.lower().str.contains(search, na=False))
        df_title_filtrer = pd.concat([df_title[titre_exact].sort_values(by="startYear", ascending=False), df_title[titre_partielle].sort_values(by="startYear", ascending=False)])

    except:
        pass

    if search:

        liste_id_imdb = [id for id in df_title_filtrer['tconst'].unique()]
        dic_poster = {}
        for idx, id in enumerate(liste_id_imdb):
            if idx < 30 :

                url = "https://api.themoviedb.org/3/find/"+id+"?external_source=imdb_id&language=fr-FR"

                response = requests.get(url, headers=headers)

                data = json.loads(response.text)
                #st.write(data)

                try:
                    dic_poster[id] = data["movie_results"][0]["poster_path"]
                except:
                    pass
    
        cols = st.columns(3)

        for idx, (id_imdb, poster) in enumerate(dic_poster.items()):
            if poster is not None:
                col = cols[idx % 3]
                with col:
                    with st.container():
                        st.image("https://image.tmdb.org/t/p/w500/" + poster)

                        if st.button("Cliquer ici pour plus d'informations", key=id_imdb,use_container_width=True):    
                            st.session_state['selected_film'] = id_imdb
                            st.switch_page("pages/page_film.py")  

elif selected == "Acteur": 
    search2 = st.text_input("Search movies by actor", value="").lower()

    #Changement d'approche je préfert qu'il commence par les lettre a la place de il contient.
    if search2:
        #Je force l'utilisateur a écrire le nom et le prénom car sinon il y a trop de possibilité si on écrit uniquement Tom par exemple
        if len(search2.split()) < 2:    
            st.warning("Veuillez entrer le **prénom et le nom** pour une recherche plus précise.")
        else:
            actorName = df_info["primaryName"].str.lower().str.contains(search2, na=False) & ((df_info["category"] == "actor") | (df_info["category"] == "actress"))
            result = df_info[actorName]
            list_id_imdb = result["tconst"].tolist()
            dic_poster = {}
            for idx, id in enumerate(list_id_imdb):

                    url = "https://api.themoviedb.org/3/find/"+ id +"?external_source=imdb_id&language=fr-FR"

                    response = requests.get(url, headers=headers)

                    data = json.loads(response.text)

                    try:
                        dic_poster[id] = data["movie_results"][0]["poster_path"]
                    except:
                        pass


        cols = st.columns(3)

        for idx, (id_imdb, poster) in enumerate(dic_poster.items()):
            if poster is not None:
                col = cols[idx % 3]
                with col:
                    with st.container():
                        st.image("https://image.tmdb.org/t/p/w500/" + poster)

                        if st.button("Cliquer ici pour plus d'informations", key=id_imdb,use_container_width=True):    
                            st.session_state['selected_film'] = id_imdb
                            st.switch_page("pages/page_film.py")  

else: 
    
    search3 = st.text_input("Seach movies by realisateur",value="").lower()

    if search3:
        
        directorName = df_info["primaryName"].str.lower().str.contains(search3, na=False) & (df_info["category"] == "director")
        
        result = df_info[directorName]
        list_id_imdb = result["tconst"].tolist()
        dic_poster = {}
        for idx, id in enumerate(list_id_imdb):

                url = "https://api.themoviedb.org/3/find/"+ id +"?external_source=imdb_id&language=fr-FR"

                response = requests.get(url, headers=headers)

                data = json.loads(response.text)

                try:
                        dic_poster[id] = data["movie_results"][0]["poster_path"]
                except:
                    pass

        cols = st.columns(3)

        for idx, (id_imdb, poster) in enumerate(dic_poster.items()):
            if poster is not None:
                col = cols[idx % 3]
                with col:
                    with st.container():
                        st.image("https://image.tmdb.org/t/p/w500/" + poster)

                        if st.button("Cliquer ici pour plus d'informations", key=id_imdb, use_container_width=True):    
                            st.session_state['selected_film'] = id_imdb
                            st.switch_page("pages/page_film.py")  