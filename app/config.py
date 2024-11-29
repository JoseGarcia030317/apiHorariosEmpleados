import os
from dotenv import load_dotenv

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

class Config:
    DEBUG = os.getenv("DEBUG")
    SERVER = os.getenv("SERVER")
    DATABASE = os.getenv("DATABASE")
    USER = os.getenv("USER")
    PASSWORD = os.getenv("PASSWORD")
    API_PREFIX = os.getenv("API_PREFIX")
    PORT = os.getenv("PORT")