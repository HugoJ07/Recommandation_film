# j'importe les bibliothèque
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.pyplot import style

# j'importe les données

df_fr = pd.read_csv('df_france.csv', sep=',')
df_us = pd.read_csv('df_americains.csv', sep=',')
top_5_fr = pd.read_csv('top_5_fr.csv', sep=',')

## -------------------------------------------------------------------------------------------------------------------------##

#  répartition des genre par tranche d'age (nbre d'acteur par genre et par tranche d'age) pour les films de 2000 à nos jours
plt.figure(figsize=(10, 5))
countplot = sns.countplot(data=df_fr,
                          x='tranche_age',
                          hue='genre_principal')
plt.title("Répartition des acteurs/actrices par genres en fonction de leur tranche d'âge")
plt.xticks(rotation=45)
plt.show()
st.pyplot(countplot.get_figure())

## -------------------------------------------------------------------------------------------------------------------------##

# top 5 par genre et tranche d'age
# choix de la tranche d'age et du genre
 
## Obtenir la liste des genres et tranche age
genres = top_5_fr['genre_principal'].unique()
age = top_5_fr['tranche_age'].unique()

## Créer la boîte de sélection
selected_genre = st.selectbox('Choisissez un genre :', genres)
selected_age = st.selectbox("Choisissez la tranched'âge :", age)
 
## Filtrer les données
resultat = top_5_fr['genre_principal'].str.contains(selected_genre)  & (top_5_fr["tranche_age"] == selected_age) 
 
## Afficher les données filtrées
st.write(top_5_fr[resultat])

## -------------------------------------------------------------------------------------------------------------------------##

# Répartion des genres US:
# pivot_table pour heatmap
pivot_age_genre_en = df_us.pivot_table(index='tranche_age',
                                             columns='genre_principal',
                                             aggfunc='size',
                                             fill_value=0)

# heatmap
plt.figure(figsize=(10, 5))
heatmap = sns.heatmap(data=pivot_age_genre_en,
                      annot=True,
                      fmt="d",
                      cmap="YlGnBu")
plt.title("Nombre d'acteurs/actrices par genre et tranche d'âge pour les films américains")
plt.xticks(rotation=45)
plt.show()
st.pyplot(heatmap.get_figure())

## -------------------------------------------------------------------------------------------------------------------------##


## -------------------------------------------------------------------------------------------------------------------------##


## -------------------------------------------------------------------------------------------------------------------------##


