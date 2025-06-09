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

df_machin = pd.read_csv("Data/title_sup_1950.csv")

#st.write(df_machin)
selected = st.selectbox("Que voulez vous rechercher ?", ['Film', 'Acteur', 'Réalisateur'])


if selected == "Film":
    df_machin["originalTitle"] = df_machin["originalTitle"].str.replace(r"[^\w\s]", "", regex=True)
    search = st.text_input("Search movies by title", value="").lower()
    titre = df_machin["originalTitle"].str.lower().str.contains(search)
    df_title = df_machin[titre].reset_index()
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
                    st.image("https://image.tmdb.org/t/p/w500/" + poster)

                    if st.button("Cliquer ici pour plus d'informations", key=id_imdb,use_container_width=True):    
                        st.session_state['selected_film'] = id_imdb
                        st.switch_page("pages/page_film.py")  

#elif selected == "Acteur": 
    #search = st.text_input("Search movies by actor", value="")
else: 
    
    search2 = st.text_input("Seach movies by realisateur",value="").lower()
    df_machin2 = pd.read_csv("Data/info_film_leger.csv")
    #st.write(df_machin2)

    if search2:
        directorName = df_machin2["primaryName"].str.lower().str.contains(search2, na=False) & (df_machin2["category"] == "director")
        
        result = df_machin2[directorName]
        directorId = result["nconst"]


        list_id_director = result["nconst"].to_list()
        st.write(result)
        
        st.write(list_id_director)

