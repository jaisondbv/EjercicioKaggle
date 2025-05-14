import pandas as pd
from pymongo import MongoClient
import os
import json

# Leer datos desde archivo descargado
df = pd.read_csv('C:/Users/204/Documents/Kaggle/Movie_Data_File.csv') 

# Conexión a MongoDB Atlas
MONGO_URI = "mongodb+srv://ketihe1596:V1in9OG26SRXZqCZ@cluster0.a4qkpgi.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(MONGO_URI)
db = client['kaggle_db']
collection = db['datos_kaggle']

# Limpia y sube los datos
data = json.loads(df.to_json(orient='records'))
collection.delete_many({})  # Limpia colección si ya existía
collection.insert_many(data)

print("Datos subidos exitosamente a MongoDB Atlas.")


# ketihe1596
# V1in9OG26SRXZqCZ

# mongodb+srv://ketihe1596:V1in9OG26SRXZqCZ@cluster0.a4qkpgi.mongodb.net/