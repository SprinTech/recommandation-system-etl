import os
import requests
from dotenv import load_dotenv
import pandas as pd

load_dotenv()

BASE_URL = "https://api.themoviedb.org/3"
headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer " + os.getenv('TOKEN')
}

PARAMS = {
    "original_language": "fr-FR",
    "region": "FR",
    "with_original_language": "fr",
    "sort_by": "primary_release_date.desc",
    "release_date.lte": "2024-07-20",
    "vote_count.gte": 10,
    "vote_average.gte": 7
}


def get_film_data(page):
    PARAMS['page'] = page
    res = requests.get(BASE_URL + '/discover/movie', params=PARAMS, headers=headers)
    res.raise_for_status()
    films = res.json().get('results', [])

    key_list = ["title", "original_title", "release_date", "genre_ids", "overview", "vote_count", "vote_average"]
    filtered_films = [{k: film.get(k) for k in key_list} for film in films]
    return filtered_films


res = requests.get(BASE_URL + '/discover/movie', params=PARAMS, headers=headers)
res.raise_for_status()
page_count = res.json().get('total_pages', 1)

data = []

for i in range(1, min(page_count, 3)):
    film_data = get_film_data(i)
    data.extend(film_data)

df = pd.DataFrame(data)
print(df)
