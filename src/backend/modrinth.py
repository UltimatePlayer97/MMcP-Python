import requests

class ModrinthAPI:
    MODRINTH_BASE_URL = "https://api.modrinth.com/v2"

    def __init__(self):
        pass

    def search(self, query, filters=None):
        url = f"{self.MODRINTH_BASE_URL}/search"
        params = {"query": query}
        if filters:
            params.update(filters)
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()

    def getMod(self, modId):
        url = f"{self.MODRINTH_BASE_URL}/mod/{modId}"
        response = requests.get(url)
        response.raise_for_status()
        return response.json()

    def getModVersions(self, modId):
        url = f"{self.MODRINTH_BASE_URL}/mod/{modId}/version"
        response = requests.get(url)
        response.raise_for_status()
        return response.json()

    def getVersionFiles(self, versionId):
        url = f"{self.MODRINTH_BASE_URL}/version/{versionId}"
        response = requests.get(url)
        response.raise_for_status()
        return response.json()