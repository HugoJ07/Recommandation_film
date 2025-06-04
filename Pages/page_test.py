import streamlit as st
import pandas as pd
import requests
import json

def show():

    st.title("Bienvenue dans ma page test")

    film_id = st.session_state.get('selected_film')

    st.write(film_id)