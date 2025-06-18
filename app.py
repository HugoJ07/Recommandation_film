import streamlit as st
import requests
import json


url = "https://api.themoviedb.org/3/trending/movie/day?language=fr-FR"
url_act = f"https://api.themoviedb.org/3/movie/now_playing?language=fr-FR&page=1&region=FR"
headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIzZGJlNWFjZDc1YmIzMWVlYTE2ZmMyY2VkMjU5YmM5ZiIsIm5iZiI6MTc0ODg1OTEyMy41MDQsInN1YiI6IjY4M2Q3OGYzMzVmOGU1MjAxODUzODM2YiIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.06eO4o3IsGnUgXiyrinBOs0jUrexp-CLvKUjbJruAJY"
    }

response = requests.get(url, headers=headers)
response_act = requests.get(url_act, headers=headers)
data = json.loads(response.text)
data_act = json.loads(response_act.text)

st.set_page_config(initial_sidebar_state="collapsed")
st.markdown(
"""
<style>
    [data-testid="stMainBlockContainer"] {max-width: 950px;display:flex; align-items:center;}
    [data-testid="stSidebar"] {display: none;}
    [data-testid="stHorizontalBlock"] {display: flex; align-items:center;text-align:center;}
    [data-testid="stMarkdownContainer"] p {height: 30px; margin:2px}
    [data-testid="stMarkdownContainer"] {color :  fdf9f8  ; text-shadow: 3px 3px 14px black;}
    [data-testid="stImageContainer"] {border:2px solid black ; border-radius: 6px}

    h2,h3 {text-align: center ;}
    .stApp{
        background-image: url("https://cdn.pixabay.com/photo/2018/01/14/23/12/nature-3082832_1280.jpg");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        display:flex; 
        align-items:center;
    }

</style>
""", 
unsafe_allow_html=True)

st.header("Bienvenue sur l'app Ciné CreusInfo !")
#st.write(data_act["results"])
st.session_state['selected_film'] = None

st.image("Data/4d09a4ec-f506-4841-8c2d-7fb803356827.jpg")

list_poster = []
list_title = []

for idx in range(0,6):
    #st.write(data["results"][idx])
    list_poster.append(data["results"][idx]["poster_path"])
    list_title.append(data["results"][idx]["title"])

#st.write(list_poster)
#st.write(list_title)

if st.button("Commencer votre expérience",use_container_width=True):
    st.session_state["bouton_reco"] = False
    st.switch_page("pages/recherche_film.py")


st.markdown(
        f'''
        <h3>Les films qui font parler en ce moment !</h3>
        ''',
        unsafe_allow_html=True)
cols = st.columns(5)

for idx in range(len(list_poster)-1):
    with cols[idx]:
        url_img = "https://image.tmdb.org/t/p/w500/" + list_poster[idx]
        title = list_title[idx]
        st.markdown(
                f'''
                <img src="{url_img}" style="height:250px; width:100%; display:block; margin-left:auto; margin-right:auto;border:2px solid black; border-radius: 8px; margin-bottom : 15px;" />
                ''',
                unsafe_allow_html=True)
        st.write(title)

list_poster2 = []
list_title2 = []

for idx in range(0,6):
    #st.write(data["results"][idx])
    list_poster2.append(data_act["results"][idx]["poster_path"])
    list_title2.append(data_act["results"][idx]["title"])

#st.write(list_poster2)
#st.write(list_title2)

st.markdown(
        f'''
        <h3>Les films actuellement au cinéma !</h3>
        ''',
        unsafe_allow_html=True)
cols = st.columns(5)

for idx in range(len(list_poster2)-1):
    with cols[idx]:
        url_img2 = "https://image.tmdb.org/t/p/w500/" + list_poster2[idx]
        title = list_title2[idx]
        st.markdown(
                f'''
                <img src="{url_img2}" style="height:250px; width:100%; display:block; margin-left:auto; margin-right:auto;border:2px solid black; border-radius: 8px; margin-bottom : 15px;" />
                ''',
                unsafe_allow_html=True)
        st.write(title)



# # Initialisation de la session state
# if 'page' not in st.session_state:
#     st.session_state['page'] = 'recherche_film'
# if 'select_film' not in st.session_state:
#     st.session_state['select_film'] = None

# # Navigation manuelle
# if st.session_state['page'] == 'recherche_film':
#     recherche_film.show()
# elif st.session_state['page'] == 'page_film':
#     page_film.show()
