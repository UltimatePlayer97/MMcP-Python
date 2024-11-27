from fastapi import FastAPI
from modrinth import searchModrinth, getModrinthMod
from curseforge import searchCurseForge, getCurseForgeMod

app = FastAPI()

@app.get("/modrinth/search")
def modrinSearch(query: str, limit: int = 10):
    return searchModrinth(query, {"limit": limit})

@app.get("/modrinth/mod/{modId}")
def modrinthModDetails(modId: str):
    return getModrinthMod(modId)

@app.get("/curseforge/search")
def curseforgeSearch(query: str, limit: int = 10):
    return searchCurseForge(query, {"pageSize": limit})

@app.get("/curseforge/mod/{modId}")
def curseforgeModDetails(modId: int):
    return getCurseForgeMod(modId)
