import streamlit as st
import pandas as pd
import requests
import json

st.set_page_config(initial_sidebar_state="collapsed")


headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIzZGJlNWFjZDc1YmIzMWVlYTE2ZmMyY2VkMjU5YmM5ZiIsIm5iZiI6MTc0ODg1OTEyMy41MDQsInN1YiI6IjY4M2Q3OGYzMzVmOGU1MjAxODUzODM2YiIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.06eO4o3IsGnUgXiyrinBOs0jUrexp-CLvKUjbJruAJY"
    }
st.title("Application de recommendation de film")

df_title = pd.read_csv("Data/title_sup_1950.csv")
df_info = pd.read_csv("Data/info_film_leger.csv")
#st.write(df_machin)
selected = st.selectbox("Que voulez vous rechercher ?", ['Film', 'Acteur', 'Réalisateur'])


if selected == "Film":
    df_title["originalTitle"] = df_title["originalTitle"].str.replace(r"[^\w\s]", "", regex=True)
    search = st.text_input("Search movies by title", value="").lower()
    titre = df_title["originalTitle"].str.lower().str.contains(search)
    df_title = df_title[titre].reset_index()
    if search:

        liste_id_imdb = df_title['tconst'].to_list()
        dic_poster = {}
        for idx, id in enumerate(liste_id_imdb):
            if idx < 30 :

                url = "https://api.themoviedb.org/3/find/"+ id +"?external_source=imdb_id"

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
            actorName = df_info["primaryName"].str.lower().str.startswith(search2, na=False) & ((df_info["category"] == "actor") | (df_info["category"] == "actress"))
            result = df_info[actorName]
                
            list_id_actor = result["nconst"].tolist()

            person_id = set()
            for idx,id_imdb in enumerate(list_id_actor):
                if idx < 5 :
                    try:
                        url = f"https://api.themoviedb.org/3/find/{id_imdb}?external_source=imdb_id"
                        response = requests.get(url, headers=headers)
                        data = response.json()
                        person_id.add(data["person_results"][0]["id"])
                    except:
                        pass

            list_poster = []
            list_id_tmdb = []
            list_imdb_id = []
            #st.write(person_id)
            #Ici je vais récupérer l'id imdb, le poster path et id tmdb du FILM ainsi que son posterPath. Je récupère l'id_tmdb pour récupérer l'id imdb du film pour la recherche 
            for idx , id in enumerate(list(person_id)):
                url_movies = "https://api.themoviedb.org/3/person/" + str(id) + "/movie_credits"
                response2 = requests.get(url_movies, headers=headers)
                data2 = json.loads(response2.text)

                #st.write(data2)
                for elem in data2["cast"]:
                    poster = elem["poster_path"]
                    id_tmdb = elem["id"]
                    if poster and id_tmdb:
                        list_poster.append(poster)
                        list_id_tmdb.append(id_tmdb)
                        url_id_imdb = f"https://api.themoviedb.org/3/movie/{id_tmdb}/external_ids"
                        response_imdb = requests.get(url_id_imdb, headers=headers)
                        data_imdb = json.loads(response_imdb.text)
                        
                        if data_imdb["imdb_id"] != None:
                            list_imdb_id.append(data_imdb["imdb_id"])

            cols = st.columns(3)

            for idx, (id_imdb, poster) in enumerate(zip(list_imdb_id, list_poster)):
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
    #st.write(df_machin2)

    if search3:
        
        directorName = df_info["primaryName"].str.lower().str.contains(search3, na=False) & (df_info["category"] == "director")
        
        result = df_info[directorName]
        directorId = result["nconst"]


        list_id_director = result["nconst"].to_list()
        #st.write(result)
        person_id = set()
        #st.write(list_id_director)

        for idx, id in enumerate(list_id_director):
            #Grâce avec le nconst je viens récupérer son ID tmdb (a trois chiffre)
            try:
                url = "https://api.themoviedb.org/3/find/"+ id +"?external_source=imdb_id"
                
                response = requests.get(url, headers=headers)

                data = json.loads(response.text)
                #person_id = data["person_results"][0]["id"]
                person_id.add(data["person_results"][0]["id"])
                #st.write(data)
                

            except:
                pass


        list_poster = []
        list_id_tmdb = []
        list_imdb_id = []
         #Ici je vais récupérer l'id imdb, le poster path et id tmdb du FILM ainsi que son posterPath. Je récupère l'id_tmdb pour récupérer l'id imdb du film pour la recherche 
        for idx , id in enumerate(list(person_id)):
            url_movies = "https://api.themoviedb.org/3/person/" + str(id) + "/movie_credits"
            response2 = requests.get(url_movies, headers=headers)
            data2 = json.loads(response2.text)
            for elem in data2["crew"]:
                if elem["job"] == "Director":
                    poster = elem["poster_path"]
                    id_tmdb = elem["id"]
                    if poster and id_tmdb:
                        list_poster.append(poster)
                        list_id_tmdb.append(id_tmdb)
                        url_id_imdb = f"https://api.themoviedb.org/3/movie/{id_tmdb}/external_ids"
                        response_imdb = requests.get(url_id_imdb, headers=headers)
                        data_imdb = json.loads(response_imdb.text)
                    
                        if data_imdb["imdb_id"] != None:
                            list_imdb_id.append(data_imdb["imdb_id"])


        cols = st.columns(3)

        for idx, (id_imdb, poster) in enumerate(zip(list_imdb_id, list_poster)):
            if poster is not None:
                col = cols[idx % 3]
                with col:
                    with st.container():
                        st.image("https://image.tmdb.org/t/p/w500/" + poster)

                        if st.button("Cliquer ici pour plus d'informations", key=id_imdb,use_container_width=True):    
                            st.session_state['selected_film'] = id_imdb
                            st.switch_page("pages/page_film.py")