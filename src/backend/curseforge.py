import os
import requests

CURSEFORGE_BASE_URL = "https://api.curseforge.com/v1"
API_KEY = os.getenv("CURSEFORGE_API_KEY")
MINECRAFT_GAME_ID = 432

def searchCurseForge(query, filters=None):
    url = f"{CURSEFORGE_BASE_URL}/mods/search"
    headers = {"x-api-key": API_KEY}
    params = {"gameId": MINECRAFT_GAME_ID, "searchFilter": query}
    if filters:
        params.update(filters)
    response = requests.get(url, headers=headers, params=params)
    return response.json()

def getCurseForgeMod(modId):
    url = f"{CURSEFORGE_BASE_URL}/mods/{modId}"
    headers = {"x-api-key": API_KEY}
    response = requests.get(url, headers=headers)
    return response.json()