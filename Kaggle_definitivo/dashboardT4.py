import streamlit as st
import pandas as pd
from pymongo import MongoClient
import plotly.express as px
import ast

MONGO_URI = "mongodb+srv://ketihe1596:V1in9OG26SRXZqCZ@cluster0.a4qkpgi.mongodb.net/"
client = MongoClient(MONGO_URI)
db = client['kaggle_db']
collection = db['datos_kaggle']

# Cargar datos desde MongoDB
data = list(collection.find({}, {"_id": 0}))  # Omitir el _id de MongoDB
df = pd.DataFrame(data)

# Limpiar y convertir las listas de cast y géneros de texto a listas reales
def safe_literal_eval(value):
    try:
        return ast.literal_eval(value) if value is not None else []
    except (ValueError, SyntaxError):
        return []

df['Cast'] = df['Cast'].apply(safe_literal_eval)
df['Genres'] = df['Genres'].apply(safe_literal_eval)

# Primer gráfico: actor con más apariciones
actor_appearances = {}

# Contamos las apariciones de cada actor en las películas
for cast in df['Cast']:
    for actor in cast:
        if actor in actor_appearances:
            actor_appearances[actor] += 1
        else:
            actor_appearances[actor] = 1

# Convertimos el diccionario a un DataFrame
actor_df = pd.DataFrame(list(actor_appearances.items()), columns=['Actor', 'Appearances'])

# Encontramos el actor con más apariciones
actor_df = actor_df.sort_values(by='Appearances', ascending=False)

# Gráfico de barras del actor con más apariciones
fig_actor = px.bar(actor_df.head(10), x='Actor', y='Appearances',
                   title="Top 10 Actores con más apariciones en películas",
                   labels={'Actor': 'Actor', 'Appearances': 'Número de Apariciones'})

# Segundo gráfico: Películas ordenadas de peor a mejor rankeada
sorted_movies = df[['Film_title', 'Average_rating']].sort_values(by='Average_rating', ascending=True)

# Gráfico de barras de películas de peor a mejor rankeada
fig_movies = px.bar(sorted_movies, x='Film_title', y='Average_rating',
                    title="Películas de peor a mejor rankeada",
                    labels={'Film_title': 'Película', 'Average_rating': 'Puntuación Promedio'},
                    color='Average_rating')

# Mostrar las gráficas en Streamlit
st.title("Dashboard desde MongoDB Atlas")

# Mostrar la tabla de datos
st.write(df)

# Mostrar la gráfica del actor con más apariciones
st.plotly_chart(fig_actor)

# Mostrar la gráfica de películas de peor a mejor rankeada
st.plotly_chart(fig_movies)
