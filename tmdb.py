import os
from unicodedata import name
import requests
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())  # This is to load your API keys from .env

BASE_URL = "https://api.themoviedb.org/3/movie/"
PIC_URL = "https://image.tmdb.org/t/p/w500/"


def get_movie_data(keyword):

    params = {
        "api_key": os.getenv("TMDB_KEY"),
    }
    q = BASE_URL + keyword

    response = requests.get(q, params=params)
    data = response.json()
    genres_data = data["genres"]
    genreslist = []
    for item in genres_data:
        genreslist.append(item["name"])

    picture = PIC_URL + data["poster_path"]

    return (data["title"], data["tagline"], genreslist, picture)
