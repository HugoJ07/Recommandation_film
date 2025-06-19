# j'importe les bibliothèque
import requests
import json

from datetime import datetime, timedelta

import streamlit as st
import pandas as pd
import numpy as np

import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.pyplot import style

import altair as alt

st.markdown(
"""
<style>
    [data-testid="stSidebar"] {display: none;}
    [data-testid="stMainBlockContainer"] {max-width:1000px}

</style>
""", 
unsafe_allow_html=True)

# j'importe les données

df_fr = pd.read_csv('fichiers_dashboard/df_fr.csv', sep=',')
df_us = pd.read_csv('fichiers_dashboard/df_en.csv', sep=',')
top_10_fr = pd.read_csv('fichiers_dashboard/top_10_fr.csv', sep=',')

#  les transformation faites en cours pour les visualisations
df_fr['release_year'] = df_fr['release_year'].apply(lambda x: str(x))
df_fr = df_fr[df_fr['tranche_age'] != '0 - 10']
df_fr = df_fr[df_fr['tranche_age'] != '10 - 20']

top_10_fr = top_10_fr[top_10_fr['tranche_age'] != '0 - 10']
top_10_fr = top_10_fr[top_10_fr['tranche_age'] != '10 - 20']

df_us = df_us[df_us['tranche_age'] != '0 - 10']
df_us = df_us[df_us['tranche_age'] != '10 - 20']

## -------------------------------------------------------------------------------------------------------------------------##

st.title("Cinéma : Qui Joue, Quoi Plaît ? ")
st.header (' "C’est pas parce qu’on comprend pas que c’est pas logique" ')
st.image("fichiers_dashboard/Image Pellicule.png",use_container_width=True)

# le cinéma français
st.subheader("Les acteurs du cinéma français")
st.text("Films de 2000 à nos jours")

#  répartition des genre par tranche d'age (nbre d'acteur par genre et par tranche d'age) pour les films de 2000 à nos jours

# Menu déroulant avec les genres disponibles
liste_genres = df_fr['genres_concat'].unique().tolist()
liste_genres.sort()

genre_selectionne = st.selectbox("Choisissez un genre", options=liste_genres, key="liste_genres")

# Filtrage du DataFrame selon le genre choisi
df_filtré = df_fr[df_fr['genres_concat'] == genre_selectionne]

# Création du graphique
y_max = 4500
chart = alt.Chart(df_filtré).mark_bar().encode(
                                                x=alt.X('tranche_age:N', title='Tranche d\'âge', 
                                                sort=['20 - 30', '30 - 40', '40 - 50', '50 - 60', '60 - 70', '70 - 80', '80 - 90', '90 - 100'],axis=alt.Axis(labelAngle=45)),
                                                y=alt.Y('count():Q', title='Nombre d\'acteurs', scale=alt.Scale(domain=[0, y_max])),
                                                tooltip=['tranche_age', 'count()']
                                            ).properties(
                                                        title=f"Répartition des acteurs par tranche d'âge pour le genre : {genre_selectionne}",
                                                        width=600,
                                                        height=400
                                                        )

st.altair_chart(chart, use_container_width=True)

st.image("fichiers_dashboard/Image Pellicule.png",use_container_width=True)

## -------------------------------------------------------------------------------------------------------------------------##

# # top 10 par genre et tranche d'age

st.subheader("TOP 10 des acteurs par genre et tranche d'âge")
st.text("Films de 2000 à nos jours")
## Obtenir la liste des genres et tranche age
genres = top_10_fr['genres_concat'].unique()
age = top_10_fr['tranche_age'].unique()

## Créer la boîte de sélection
selected_genre_1 = st.selectbox('Choisissez un genre :', genres, key="select_genre_1")
selected_age_1 = st.selectbox("Choisissez la tranched'âge :", age, key="select_age_1")
 
## Filtrer les données
resultat_1 = top_10_fr['genres_concat'].str.contains(selected_genre_1)  & (top_10_fr["tranche_age"] == selected_age_1) 
 
## Afficher les données filtrées
st.write(top_10_fr[resultat_1])

st.image("fichiers_dashboard/Image Pellicule.png",use_container_width=True)


## -------------------------------------------------------------------------------------------------------------------------##

# top 10 des acteurs / actrices par tranche d'age tous genres
st.subheader("TOP 10 des acteurs par tranche d'âge")
st.text("Films de 2000 à nos jours")
# df filtre de ce qui me faut
test = df_fr[['tranche_age', 'genres_concat', 'primaryName','imdb_id']]

# Comptage du nombre de films par acteur et tranche d’âge
acteur_count = test.groupby(['tranche_age', 'primaryName'])['imdb_id'].nunique().reset_index()

# Renommer la colonne
acteur_count.rename(columns={'imdb_id': 'nb_films'}, inplace=True)

# Tri : par tranche d'âge (croissant) puis par nb de films (décroissant)
acteur_count = acteur_count.sort_values(by=['tranche_age', 'nb_films'], ascending=[True, False])

# Top 10 des acteurs par tranche d'âge
top_10_acteurs = acteur_count.groupby('tranche_age').head(10)


## Obtenir la liste tranche age
age_2 = top_10_acteurs['tranche_age'].unique()

## Créer la boîte de sélection
selected_age_2 = st.selectbox("Choisissez la tranched'âge :", age_2, key="select_age_2")
 
## Filtrer les données
resultat_2 = top_10_acteurs["tranche_age"] == selected_age_2
 
## Afficher les données filtrées
st.write(top_10_acteurs[resultat_2])

st.image("fichiers_dashboard/Image Pellicule.png",use_container_width=True)

## -------------------------------------------------------------------------------------------------------------------------##
# Liste de film par acteur 
st.subheader("Les films par acteur")
st.text("Films de 2000 à nos jours")

# choix utilisateur
choix_acteur = st.selectbox("Nom de l'acteur",df_fr["primaryName"].unique())

# toutes les lignes avec le nom de l'acteur
film = df_fr[df_fr['primaryName'].str.contains(choix_acteur)]

# filtrage pour juste colonne titre et date de sortie
film_affichage = film[['primaryName', 'original_title', 'release_year']].drop_duplicates().sort_values('release_year', ascending=False)

st.write(film_affichage)


#----------------------------------------------------------FILMS ARTS ET ESSAIS 2024

#----------------------------------------------------------FILMS ARTS ET ESSAIS 2024
# LE FICHIER :
df_ae24 = pd.read_excel("fichiers_dashboard/Films_Art_Essais_2024.xlsx")
# Nettoyage de la colonne Boxoffice
df_ae24['BoxOffice'] = df_ae24['BoxOffice'].replace('NC', 0)
df_ae24['BoxOffice'] = df_ae24['BoxOffice'].astype(int)
# Fonction pour convertir les durée de films en heure en minutes :
def convertir_en_minutes(x):
    heures = int(x)
    minutes = (x - heures) * 100  # On multiplie par 100 car les minutes sont en décimal style 0.40 = 40 minutes
    return heures * 60 + minutes
# Application de la fonction de conversion heurs/minutes
df_ae24['duree_minutes'] = df_ae24['Durée'].apply(convertir_en_minutes)
df_ae24['duree_minutes'] = df_ae24['duree_minutes'].astype(int)
# Calcule de la durée moyenne des films
df_ae24['mean_duree'] = df_ae24['duree_minutes'].round(-1)
moyenne_entrees = df_ae24.groupby('mean_duree')['BoxOffice'].mean()
#--------------------------------------------------------------STREAMLIT
# ------------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------FILMS PATRIMOINE 2025
# LE FICHIER :
df_patrim25 = pd.read_excel("fichiers_dashboard/Films_Patrimoine_2025.xlsx")
# couleur des genres patrimoine dans les viz
genres = sorted(df_patrim25['Genre'].unique())    # il me faut une liste des genres
genre_palette = {
    'Comédie':'#1F77B4',
    'Action':'#D62728',
    'Drame':'#FF7F0E',
    'Documentaire':'#8C564B',
    'Thriller':'#7F7F7F',
    'Biopic':'#E377C2',
    'Aventure':'#2CA02C',
    'Fantastique':'#17BECF',
    'court-métrage':'#9467BD'
}
st.header("Les films Patrimoine en 2025")
# Visuel 1      ### Histogramme des genres
nb_films_par_genre = df_patrim25.groupby('Genre')['Film'].count()
st.subheader('Les films patrimoine réédités en 2025 par genre')
plt.figure(figsize=(10,5))
sns.barplot(data=nb_films_par_genre, palette=genre_palette)
plt.title("Nombre de films patrimoine par genre réédités en 2025")
plt.xlabel('Genre')
plt.ylabel('Nombre de films')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
st.pyplot(plt.gcf())
# Visuel 2 PAT      ### Histogramme par décénie et par genre
# le nombre de genre par année de création
df_patrim25['periode'] = (df_patrim25['Sortie initiale']//10)*10
# j'importe matplotlib.ticker afin d'avoir l'echelle de l'axe y en nombre entier
from matplotlib.ticker import MaxNLocator, MultipleLocator
st.subheader('Les films patrimoine par périodes de réalisation')
plt.figure(figsize=(10,5))
sns.countplot(data=df_patrim25, x='periode', hue='Genre', palette=genre_palette, hue_order=genres)
plt.title("Nombre de films patrimoine par genre et par décénie de réalisation")
plt.xlabel('Période de réalisation')
plt.ylabel('Nombre de films')
plt.ylim(0, 25)
plt.gca().yaxis.set_major_locator(MaxNLocator(integer=True))
plt.gca().yaxis.set_major_locator(MultipleLocator(5))
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
st.pyplot(plt.gcf())
# Visuel 3 PAT      ### Histogramme du Nombre de films patrimoine par pays
st.subheader('Les films patrimoine par pays')
plt.figure(figsize=(10,5))
sns.countplot(data=df_patrim25, x='Origin', order=(df_patrim25['Origin'].value_counts().sort_values(ascending=False).index))
plt.title("Nombre de films patrimoine par pays")
plt.xlabel('Pays')
plt.ylabel('Nombre de films')
plt.ylim(0, 25)
plt.gca().yaxis.set_major_locator(MaxNLocator(integer=True))
plt.gca().yaxis.set_major_locator(MultipleLocator(5))
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
st.pyplot(plt.gcf())
# Visuel 4 PAT     ### les films patrimoine classé par pays
st.subheader('Les films patrimoine par genres et par pays')
plt.figure(figsize=(10,5))
sns.countplot(data=df_patrim25, x='Origin', hue='Genre', palette=genre_palette, hue_order=genres, order=(df_patrim25['Origin'].value_counts().sort_values(ascending=False).index))
plt.title("Nombre de genres de films patrimoine par pays")
plt.xlabel('Pays')
plt.ylabel('Nombre de films')
plt.ylim(0, 25)
plt.gca().yaxis.set_major_locator(MaxNLocator(integer=True))
plt.gca().yaxis.set_major_locator(MultipleLocator(5))
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
st.pyplot(plt.gcf())
#-------------------------------------------------------------------------------------------------------------------------------------
# FILMS ARTS ET ESSAIS 2024
# Titre
st.header("Les films Art & Essais")
# couleur des genres A&E dans les viz
genres_ae = sorted(df_ae24['Genre'].unique())
genre_ae_palette = {
    'Comédie':'#1F77B4',
    'Musical':'#C49C94',
    'Drame':'#FF7F0E',
    'Documentaire':'#8C564B',
    'Thriller':'#7F7F7F',
    'Biopic':'#E377C2',
    'Animation':'#9EDAE5',
    'Horreur':'#BCBD22'
}
# Visuel 1 AE      ### Histogramme du boxoffice par genre
st.subheader('Le Boxoffice des films Art & Essais par genre')
plt.figure(figsize=(10,5))
sns.barplot(data=df_ae24, x='Genre', y='BoxOffice', ci=None, palette=genre_ae_palette, order=genres_ae)
plt.title("Nombre d'entrée par genre de films Art & Essais en 2024")
plt.xlabel('Genre du film classé Art & Essais')
plt.ylabel('Box Office')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
st.pyplot(plt.gcf())
#Visuel 2 AE       ### Histogramme du nombre de films Art & Essais par pays
st.subheader('Les films Art & Essais par pays')
plt.figure(figsize=(10,5))
sns.countplot(data=df_ae24, x='Origin',order=(df_ae24['Origin'].value_counts().sort_values(ascending=False).index))
plt.title("Nombre de films Art & Essais par pays")
plt.xlabel('Pays')
plt.ylabel('Nombre de films')
plt.ylim(0, 20)
plt.gca().yaxis.set_major_locator(MaxNLocator(integer=True))
plt.gca().yaxis.set_major_locator(MultipleLocator(5))
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
st.pyplot(plt.gcf())
# Visuel 3 AE      ### les films Art & Essais par genre et par pays
st.subheader('Les films Art & Essais par genres et par pays')
plt.figure(figsize=(10,5))
sns.countplot(data=df_ae24, x='Origin', hue='Genre', palette=genre_ae_palette, hue_order=genres_ae, order=(df_ae24['Origin'].value_counts().sort_values(ascending=False).index))
plt.title("Nombre de genres de films patrimoine par pays")
plt.xlabel('Pays')
plt.ylabel('Nombre de films')
plt.ylim(0, 20)
plt.gca().yaxis.set_major_locator(MaxNLocator(integer=True))
plt.gca().yaxis.set_major_locator(MultipleLocator(5))
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
st.pyplot(plt.gcf())











st.image("fichiers_dashboard/Image Pellicule.png",use_container_width=True)

# Répartion des genres US:

st.subheader("Clap de fin avec les acteurs américains par genre et tranche d’âge")
st.text("Films de 2000 à nos jours")

# Menu déroulant avec les genres disponibles
liste_genres_us = df_us['genres_concat'].unique().tolist()
liste_genres_us.sort()

genre_selectionne_us = st.selectbox("Choisissez un genre", options=liste_genres_us, key="liste_genres_us")

# Filtrage du DataFrame selon le genre choisi
df_filtré_us = df_us[df_us['genres_concat'] == genre_selectionne_us]
df_filtré_us = df_filtré_us[df_filtré_us['tranche_age'].notna()]

# Création du graphique

# Création du graphique
y_max = 30000
chart_us = alt.Chart(df_filtré_us).mark_bar().encode(
                                                x=alt.X('tranche_age:N', title='Tranche d\'âge', 
                                                sort=['20 - 30', '30 - 40', '40 - 50', '50 - 60', '60 - 70', '70 - 80', '80 - 90', '90 - 100'],axis=alt.Axis(labelAngle=45)),
                                                y=alt.Y('count():Q', title='Nombre d\'acteurs', scale=alt.Scale(domain=[0, y_max])),
                                                tooltip=['tranche_age', 'count()']
                                            ).properties(
                                                        title=f"Répartition des acteurs par tranche d'âge pour le genre : {genre_selectionne_us}",
                                                        width=600,
                                                        height=400
                                                        )

st.altair_chart(chart_us, use_container_width=True)

cols = st.columns(3)

with cols[1]:
    st.image("fichiers_dashboard/Image clap.png")

## -------------------------------------------------------------------------------------------------------------------------##


## -------------------------------------------------------------------------------------------------------------------------##


## -------------------------------------------------------------------------------------------------------------------------##

