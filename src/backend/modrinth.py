import requests

MODRINTH_BASE_URL = "https://api.modrinth.com/v2"

def searchModrinth(query, filters=None):
    url = f"{MODRINTH_BASE_URL}/search"
    params = {"query:": query}
    if filters:
        params.update(filters)
    response = requests.get(url, params=params)
    return response.json()

def getModrinthMod(modId):
    url = f"{MODRINTH_BASE_URL}/mod/{modId}"
    response = requests.get(url)
    return response.json()
