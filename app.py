import streamlit as st

st.set_page_config(initial_sidebar_state="collapsed")

st.title("Bienvenue sur l'app Ciné CreusInfo !!:clapper::clapper::clapper:")

st.image("Data/4d09a4ec-f506-4841-8c2d-7fb803356827.jpg")


st.session_state['selected_film'] = None

if st.button("Commencer votre expérience", use_container_width=True):
    st.switch_page("pages/recherche_film.py")



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
