import json
import requests

BASE_URL = "https://en.wikipedia.org/w/api.php"


def get_link(title):
    params = {"action": "opensearch", "search": title, "format": "json"}
    response = requests.get(BASE_URL, params=params)
    data = response.json()
    website_data = data[3][0]
    return website_data
