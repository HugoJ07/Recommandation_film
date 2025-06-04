import streamlit as st

#from Pages import page_film
from Pages import recherche_film
from Pages import page_test

# Initialisation de la session state
if 'page' not in st.session_state:
    st.session_state['page'] = 'recherche_film'
if 'selected_film' not in st.session_state:
    st.session_state['selected_film'] = None
#st.write("Page actuelle:", st.session_state['page'])
# Navigation manuelle
if st.session_state['page'] == 'recherche_film':
    recherche_film.show()
#elif st.session_state['page'] == 'description':
#    page_film.show()
elif st.session_state['page'] == 'test':
    page_test.show()