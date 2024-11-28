import os
import requests

class CurseForgeAPI:
    CURSEFORGE_BASE_URL = "https://api.curseforge.com/v1"
    GAME_ID = 432

    API_KEY = os.getenv("CURSEFORGE_API_KEY")

    def __init__(self, API_KEY):
        if not API_KEY:
            raise ValueError("API key is required for CurseForge.")

    def search(self, query, filters=None):
        url = f"{self.CURSEFORGE_BASE_URL}/mods/search"
        headers = {"x-api-key": self.API_KEY}
        params = {"gameId": self.GAME_ID, "searchFilter": query}
        if filters:
            params.update(filters)
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        return response.json()

    def getMod(self, modId):
        url = f"{self.CURSEFORGE_BASE_URL}/mods/{modId}"
        headers = {"x-api-key": self.API_KEY}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()

    def getModVersions(self, modId):
        url = f"{self.CURSEFORGE_BASE_URL}/mods/{modId}/files"
        headers = {"x-api-key": self.API_KEY}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json().get("data", [])

    def getVersionFiles(self, modId, fileId):
        url = f"{self.CURSEFORGE_BASE_URL}/mods/{modId}/files/{fileId}"
        headers = {"x-api-key": self.API_KEY}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json().get("data", {})
