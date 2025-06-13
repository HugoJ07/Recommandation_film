# j'importe les bibliothèque
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.pyplot import style

st.markdown(
"""
<style>
    [data-testid="stSidebar"] {display: none;}
    
</style>
""", 
unsafe_allow_html=True)

# j'importe les données

df_fr = pd.read_csv('df_fr.csv', sep=',')
df_us = pd.read_csv('df_en.csv', sep=',')
top_10_fr = pd.read_csv('top_10_fr.csv', sep=',')

## -------------------------------------------------------------------------------------------------------------------------##

st.title("Cinéma : Qui Joue, Quoi Plaît ? ")
st.header (' "C’est pas parce qu’on comprend pas que c’est pas logique" ')
st.image("Image Pellicule.png")

# introduction etude de marché
st.header("Les cinémas Creusois en chiffres")
st.image("Cinémas Creuse.png")

st.image("Image Pellicule.png")

# le cinéma français
st.subheader("Les acteurs du cinéma français")
st.text("Films de 2000 à nos jours")

## -------------------------------------------------------------------------------------------------------------------------##

#  répartition des genre par tranche d'age (nbre d'acteur par genre et par tranche d'age) pour les films de 2000 à nos jours

# POUR AVOIR LES TRANCHES D'AGE EN ORDRE CHRONOLOGIQUE
# Définir l'ordre souhaité
ordre_tranches = ['0 - 10', '10 - 20', '20 - 30', '30 - 40',
                  '40 - 50', '50 - 60', '60 - 70', '70 - 80', '80 - 90', '90 - 100']

# Convertir la colonne en catégorie ordonnée
df_fr['tranche_age'] = pd.Categorical(df_fr['tranche_age'],
                                      categories=ordre_tranches,
                                      ordered=True)

couleurs = {'Comedy':'#1F77B4',
            'Action':'#D62728',
            'Drama':'#FF7F0E',
            'Thriller':'#7F7F7F',
            'ScienceFiction':'#17BECF',
            'Crime':'#FF9896',
            'Family':'#98DF8A',
            'Romance':'#F7B6D2',
            }


plt.figure(figsize=(10, 5))
countplot = sns.countplot(data=df_fr,
                          x='tranche_age',
                          hue='genres_concat',
                          palette= couleurs
                          )
plt.title("Répartition des acteurs/actrices par genres en fonction de leur tranche d'âge")
plt.xticks(rotation=45)
plt.xlabel("Tranches d'ages")
plt.ylabel("Nombre d'acteurs")
plt.show()
st.pyplot(countplot.get_figure())

st.image("Image Pellicule.png")

## -------------------------------------------------------------------------------------------------------------------------##

# top 10 par genre et tranche d'age

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

st.image("Image Pellicule.png")

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

st.image("Image Pellicule.png")


## -------------------------------------------------------------------------------------------------------------------------##


#----------------------------------------------------------FILMS ARTS ET ESSAIS 2024

# LE FICHIER :
df_ae24 = pd.read_excel("Films_Art_Essais_2024.xlsx")

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
# -------------------------------------------------------------
# FILMS ARTS ET ESSAIS 2024

# Titre
st.header("Les films Art & Essais")
st.image("subventions.png")

# couleur des genres A&E dans les viz
genres_ae = sorted(df_ae24['Genre'].unique())

genre_ae_palette = {    
    'Comédie':'#1F77B4',
    'Musical':'#C49C94',
    'Drame':'#FF7F0E',
    'Documentaire':'#8C564B',
    'Thriller':'#7F7F7F',
    'Biopic':'#E377C2',
    'Jeune Public':'#9EDAE5',
    'Horreur':'#BCBD22'  
}

# Visuel 1       ### Histogramme du boxoffice par genre
st.subheader('Le Boxoffice des films Art & Essais en 2024 en fonction du genre')

from matplotlib.ticker import FuncFormatter
# Agrégation du BoxOffice par genre
boxoffice_par_genre = df_ae24.groupby('Genre')['BoxOffice'].sum().sort_values(ascending=False)
# Fonction de formatage en millions
def millions(x, _):
    if x >= 1_000_000:
        return f'{x/1_000_000:.1f} M'.replace('.', ',')  # "2,0 M" pour 2 millions
    elif x >= 100_000:
        return f'{x/1_000_000:.1f} M'.replace('.', ',')  # "0,5 M" pour 500 000
    else:
        return f'{int(x):,}'.replace(',', ' ')  # Valeur brute si < 100 000
# Création du plot avec les données agrégées
plt.figure(figsize=(10,5))
sns.barplot(
    x=boxoffice_par_genre.index,
    y=boxoffice_par_genre.values,
    palette=genre_ae_palette
)
# Application du format personnalisé
plt.gca().yaxis.set_major_formatter(FuncFormatter(millions))
plt.title("Nombre d'entrées par genre de films Art & Essais en 2024")
plt.xlabel('Genre')
plt.ylabel('Box Office')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

st.pyplot(plt.gcf())

#----------------------------------------------------------FILMS PATRIMOINE 2025

# LE FICHIER :
df_patrim25 = pd.read_excel("Films_Patrimoine_2025.xlsx")

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

# Visuel 4      ### Histogramme des genres 
nb_films_par_genre = df_patrim25.groupby('Genre')['Film'].count()

st.subheader("Les films patrimoine réédités en 2025 classés par genre")
plt.figure(figsize=(10,5))
sns.barplot(data=nb_films_par_genre, palette=genre_palette)
plt.title("Nombre de film patrimoine par genre à l'affiche en 2025")
plt.xlabel('Genre du film classée Patrimoine')
plt.ylabel('Nombre de film par genre')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

st.pyplot(plt.gcf())

st.image("Image Pellicule.png")


# Visuel 6      ### Histogramme par décénie et par genre

# le nombre de genre par année de création
df_patrim25['periode'] = (df_patrim25['Sortie initiale']//10)*10

# j'importe matplotlib.ticker afin d'avoir l'echelle de l'axe y en nombre entier
from matplotlib.ticker import MaxNLocator, MultipleLocator

st.subheader('Les films patrimoine réédités en 2025 selon leurs périodes de réalisation') 

plt.figure(figsize=(10,5))
sns.countplot(data=df_patrim25, x='periode', hue='Genre', palette=genre_palette, hue_order=genres)
plt.title("Nombre de films patrimoine réédités en 2025    (classés par genre et par décénie de réalisation)")
plt.xlabel('Période de réalisation')
plt.ylabel('Nombre de films réalisés')
plt.ylim(0, 25)
plt.gca().yaxis.set_major_locator(MaxNLocator(integer=True))
plt.gca().yaxis.set_major_locator(MultipleLocator(5))
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

st.pyplot(plt.gcf())

st.image("Image Pellicule.png")

# Répartion des genres US:

st.subheader("Répartitions des acteurs par genre et tranche d'âge pour les films americains")
st.text("Films de 2000 à nos jours")

# POUR AVOIR LES TRANCHES D'AGE EN ORDRE CHRONOLOGIQUE
# Définir l'ordre souhaité
ordre_tranches = ['0 - 10', '10 - 20', '20 - 30', '30 - 40',
                  '40 - 50', '50 - 60', '60 - 70', '70 - 80', '80 - 90', '90 - 100']

# Convertir la colonne en catégorie ordonnée
df_us['tranche_age'] = pd.Categorical(df_us['tranche_age'],
                                      categories=ordre_tranches,
                                      ordered=True)

# countplot us
plt.figure(figsize=(10, 5))
countplot_us = sns.countplot(data=df_us,
                          x='tranche_age',
                          hue='genres_concat',
                          palette= couleurs
                          )
plt.title("Répartition des acteurs/actrices par genres en fonction de leur tranche d'âge")
plt.xticks(rotation=45)
plt.xlabel("Tranches d'ages")
plt.ylabel("Nombre d'acteurs")
plt.show()
st.pyplot(countplot_us.get_figure())


st.image("Image Pellicule.png")

## -------------------------------------------------------------------------------------------------------------------------##


## -------------------------------------------------------------------------------------------------------------------------##


## -------------------------------------------------------------------------------------------------------------------------##

