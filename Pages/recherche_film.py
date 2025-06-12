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

df_machin = pd.read_csv("Data/title_sup_1950.csv")
df_machin["title"] = df_machin["title"].str.replace(r"[^\w]", "", regex=True)
df_machin["originalTitle"] = df_machin["originalTitle"].str.replace(r"[^\w]", "", regex=True)

selected = st.selectbox("Que voulez vous rechercher ?", ['Film', 'Acteur', 'Réalisateur'])


if selected == "Film":
    try :
        
        search = st.text_input("Rechercher par titre de film", value="").lower()
        search = re.sub(r"[^\w]", "", search)
        titre_exact = (df_machin["title"].str.lower() == search) | (df_machin["originalTitle"].str.lower() == search)
        titre_partielle = (df_machin["title"].str.lower().str.contains(search, na=False)) | (df_machin["originalTitle"].str.lower().str.contains(search, na=False))
        df_title = pd.concat([df_machin[titre_exact].sort_values(by="startYear", ascending=False), df_machin[titre_partielle].sort_values(by="startYear", ascending=False)])
        

    except:
        pass

    if search:

        liste_id_imdb = [id for id in df_title['tconst'].unique()]
        dic_poster = {}
        for idx, id in enumerate(liste_id_imdb):
            if idx < 30 :

                url = "https://api.themoviedb.org/3/find/"+id+"?external_source=imdb_id&language=fr-FR"

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
                    st.image("https://image.tmdb.org/t/p/w500/" + poster)

                    if st.button("Cliquer ici pour plus d'informations", key=id_imdb):    
                        st.session_state['selected_film'] = id_imdb
                        st.switch_page("pages/page_film.py")  

# elif selected == "Acteur": 
#     search = st.text_input("Search movies by actor", value="")

# else: 
#     search = st.text_input("Seach movies by realisateur",value="")
