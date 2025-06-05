import streamlit as st

st.set_page_config(initial_sidebar_state="collapsed")

st.header("Bienvenue sur l'app Ciné CreusInfo !!!!")

st.session_state['selected_film'] = None


if st.button("Commencer votre expérience:"):
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
