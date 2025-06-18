import streamlit as st
import pandas as pd
import requests
import json
import re

st.set_page_config(initial_sidebar_state="collapsed")
#header {visibility: hidden;}
#[data-testid="stBaseButton-headerNoPadding"] {display: none;}
st.markdown(
"""
<style>
    [data-testid="stSidebar"] {display: none;}
    header {visibility: hidden;}
    .stApp{
        background-image: url("https://static.vecteezy.com/ti/vecteur-libre/p1/16265425-salle-de-cinema-avec-ecran-blanc-rideaux-sieges-gratuit-vectoriel.jpg");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
    }

    label {
        color: rgb(19, 23, 32) !important;
    }
    [data-testid="stMainBlockContainer"] {max-width: 950px;}
    [data-testid="stMarkdownContainer"] {
        display:flex;
        flex-direction:column;
        padding-top:5px;
        margin-bottom:5px;
        text-shadow: 1px 1px 1px  #302e2e ;
    }

</style>
""", 
unsafe_allow_html=True)


headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIzZGJlNWFjZDc1YmIzMWVlYTE2ZmMyY2VkMjU5YmM5ZiIsIm5iZiI6MTc0ODg1OTEyMy41MDQsInN1YiI6IjY4M2Q3OGYzMzVmOGU1MjAxODUzODM2YiIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.06eO4o3IsGnUgXiyrinBOs0jUrexp-CLvKUjbJruAJY"
    }
st.markdown(
    "<h1 style='text-align: center; color:rgb(19, 23, 32);background-color: rgba(255, 255, 255, 0.5);border-radius: 8px; padding:15px;margin-bottom:20px';>Application de recommendation de film</h1>",
    unsafe_allow_html=True
)

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
        dic_title = {}
        dic_release = {}
        dic_note = {}
        for idx, id in enumerate(liste_id_imdb):
            if idx < 30 :

                url = "https://api.themoviedb.org/3/find/"+id+"?external_source=imdb_id&language=fr-FR"

                response = requests.get(url, headers=headers)

                data = json.loads(response.text)
                #st.write(data)

                try:
                    dic_poster[id] = data["movie_results"][0]["poster_path"]
                    dic_title[id] = data["movie_results"][0]["title"]
                    dic_release[id] = data["movie_results"][0]["release_date"]
                    dic_note[id] = data["movie_results"][0]["vote_average"]
                except:
                    pass
    
        cols = st.columns(3)

        for idx, (id_imdb, poster) in enumerate(dic_poster.items()):
            if poster is not None:
                col = cols[idx % 3]
                with col:
                    with st.container():
                        url_img = "https://image.tmdb.org/t/p/w500/" + poster
                        st.markdown(
                            f'''
                            <div style="display: inline-block; border-radius: 6px">
                                <img src="{url_img}" style="height:350px; width:auto; display:block; margin-left:auto; margin-right:auto;border: 2px solid black; border-radius: 12px" />
                            </div>
                            ''',
                            unsafe_allow_html=True
                        )
                        
                        titre = dic_title.get(id_imdb)
                        date = dic_release.get(id_imdb)
                        note = dic_note.get(id_imdb)
                        st.markdown(
                            f"""
                                <div style='
                                            height: 120px;
                                            width: 280px;
                                            display: flex;
                                            flex-direction: column;
                                            justify-content: center;
                                            text-align: center;
                                            margin: 0 auto;
                                            margin-bottom: 10px;
                                            background-color: rgba(19, 23, 32, 0.7);
                                            border-radius: 12px;
                                            padding-top: 10px;
                                            padding-bottom: 20px;
                                            color: white;
                                        '>
                                <p style='margin: 8px;'>{titre}</p>
                                <p style='margin: 0;'>Date de sortie : {date}</p>
                                <p style='margin: 0;'>Note : {note:.2f}</p>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )
                        if st.button("Cliquer ici pour plus d'informations", key=id_imdb,use_container_width=True):    
                            st.session_state['selected_film'] = id_imdb
                            st.switch_page("pages/page_film.py")  

elif selected == "Acteur": 
    search2 = st.text_input("Recherche par nom d'acteur/actrice", value="").lower()

    #Changement d'approche je préfert qu'il commence par les lettre a la place de il contient.
    if search2:
        #Je force l'utilisateur a écrire le nom et le prénom car sinon il y a trop de possibilité si on écrit uniquement Tom par exemple
        if len(search2.split()) < 2:    
            st.warning("Veuillez entrer le **prénom et le nom** pour une recherche plus précise.")
        else:
            actorName = df_info["primaryName"].str.lower().str.contains(search2, na=False) & ((df_info["category"] == "actor") | (df_info["category"] == "actress"))
            result = df_info[actorName]
            #st.write(result)
            list_id_imdb = result["tconst"].tolist()
            dic_poster = {}
            dic_title = {}
            dic_release = {}
            dic_note = {}

            for idx, id in enumerate(list_id_imdb):
                    url = "https://api.themoviedb.org/3/find/"+ id +"?external_source=imdb_id&language=fr-FR"

                    response = requests.get(url, headers=headers)

                    data = json.loads(response.text)

                    try:
                        dic_poster[id] = data["movie_results"][0]["poster_path"]
                        dic_title[id] = data["movie_results"][0]["title"]
                        dic_release[id] = data["movie_results"][0]["release_date"]
                        dic_note[id] = data["movie_results"][0]["vote_average"]
                    except:
                        pass


        cols = st.columns(3)

        for idx, (id_imdb, poster) in enumerate(list(dic_poster.items())[::-1]):
            if poster is not None:
                col = cols[idx % 3]
                with col:
                    with st.container():
                        url_img = "https://image.tmdb.org/t/p/w500/" + poster
                        st.markdown(
                            f'''
                            <div style="display: inline-block; border-radius: 6px">
                                <img src="{url_img}" style="height:350px; width:auto; display:block; margin-left:auto; margin-right:auto; border-radius: 12px;padding-top:5px" />
                            </div>
                            ''',
                            unsafe_allow_html=True
                        )

                        titre = dic_title.get(id_imdb)
                        date = dic_release.get(id_imdb)
                        note = dic_note.get(id_imdb)
                        st.markdown(
                            f"""
                                <div style='
                                            height: 120px;
                                            width: 280px;
                                            display: flex;
                                            flex-direction: column;
                                            justify-content: center;
                                            text-align: center;
                                            margin: 0 auto;
                                            margin-bottom: 10px;
                                            background-color: rgba(19, 23, 32, 0.7);
                                            border-radius: 12px;
                                            padding-top: 10px;
                                            padding-bottom: 20px;
                                            color: white;
                                        '>
                                <p style='margin: 8px;'>{titre}</p>
                                <p style='margin: 0;'>Date de sortie : {date}</p>
                                <p style='margin: 0;'>Note : {note:.2f}</p>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )
                        if st.button("Cliquer ici pour plus d'informations", key=id_imdb,use_container_width=True):    
                            st.session_state['selected_film'] = id_imdb
                            st.switch_page("pages/page_film.py")  

else: 
    
    search3 = st.text_input("Récherche par realisateur",value="").lower()

    if search3:
        
        directorName = df_info["primaryName"].str.lower().str.contains(search3, na=False) & (df_info["category"] == "director")
        
        result = df_info[directorName]
        list_id_imdb = result["tconst"].tolist()
        dic_poster = {}
        dic_title = {}
        dic_release = {}
        dic_note = {}

        for idx, id in enumerate(list_id_imdb):

                url = "https://api.themoviedb.org/3/find/"+ id +"?external_source=imdb_id&language=fr-FR"

                response = requests.get(url, headers=headers)

                data = json.loads(response.text)

                try:
                        dic_poster[id] = data["movie_results"][0]["poster_path"]
                        dic_title[id] = data["movie_results"][0]["title"]
                        dic_release[id] = data["movie_results"][0]["release_date"]
                        dic_note[id] = data["movie_results"][0]["vote_average"]
                except:
                    pass

        cols = st.columns(3)

        for idx, (id_imdb, poster) in enumerate(list(dic_poster.items())[::-1]):
            if poster is not None:
                col = cols[idx % 3]
                with col:
                    with st.container():
                        url_img = "https://image.tmdb.org/t/p/w500/" + poster
                        st.markdown(
                            f'''
                            <div style="display: inline-block; border-radius: 6px">
                                <img src="{url_img}" style="height:350px; width:auto; display:block; margin-left:auto; margin-right:auto; border-radius: 12px;padding-top:5px" />
                            </div>
                            ''',
                            unsafe_allow_html=True
                        )
                        
                        titre = dic_title.get(id_imdb)
                        date = dic_release.get(id_imdb)
                        note = dic_note.get(id_imdb)
                        st.markdown(
                            f"""
                                <div style='
                                            height: 120px;
                                            width: 280px;
                                            display: flex;
                                            flex-direction: column;
                                            justify-content: center;
                                            text-align: center;
                                            margin: 0 auto;
                                            margin-bottom: 10px;
                                            background-color: rgba(19, 23, 32, 0.7);
                                            border-radius: 12px;
                                            padding-top: 10px;
                                            padding-bottom: 20px;
                                            color: white;
                                        '>
                                <p style='margin: 8px;'>{titre}</p>
                                <p style='margin: 0;'>Date de sortie : {date}</p>
                                <p style='margin: 0;'>Note : {note:.2f}</p>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )
                        if st.button("Cliquer ici pour plus d'informations", key=id_imdb,use_container_width=True):    
                            st.session_state['selected_film'] = id_imdb
                            st.switch_page("pages/page_film.py")  