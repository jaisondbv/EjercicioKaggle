import streamlit as st
from pymongo import MongoClient
import pandas as pd
import os

MONGO_URI = "mongodb+srv://ketihe1596:V1in9OG26SRXZqCZ@cluster0.a4qkpgi.mongodb.net/"
client = MongoClient(MONGO_URI)
db = client['kaggle_db']
collection = db['datos_kaggle']

# Cargar datos
data = list(collection.find({}, {"_id": 0})) 
df = pd.DataFrame(data)

st.title("Dashboard desde MongoDB Atlas")
st.write(df)

# docker run  -e MONGO_URI="mongodb+srv://ketihe1596:V1in9OG26SRXZqCZ@cluster0.a4qkpgi.mongodb.net/" etl_app
