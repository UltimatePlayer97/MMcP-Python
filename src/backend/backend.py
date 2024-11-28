import requests
from flask import Flask, request, jsonify
from modrinth import ModrinthApi
from curseforge import CurseForgeApi


app = Flask(__name__)

modrinthApi = ModrinthApi()
curseforgeApi = CurseForgeApi()

@app.route("/modrinth/search", methods=["GET"])
def modrinthSearch():
    query = request.args.get("query")
    limit = request.args.get("limit", 10, type=int)
    filters = {"limit": limit}
    try:
        result = modrinthApi.search(query, filters)
        return jsonify(result)
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500

@app.route("/modrinth/mod/<modId>", methods=["GET"])
def modrinthModDetails(modId):
    try:
        result = modrinthApi.getMod(modId)
        return jsonify(result)
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500

@app.route("/modrinth/mod/<modId>/versions", methods=["GET"])
def modrinthModVersions(modId):
    try:
        result = modrinthApi.getModVersions(modId)
        return jsonify(result)
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500

@app.route("/modrinth/version/<versionId>/files", methods=["GET"])
def modrinthVersionFiles(versionId):
    try:
        result = modrinthApi.getVersionFiles(versionId)
        return jsonify(result)
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500

@app.route("/curseforge/search", methods=["GET"])
def curseforgeSearch():
    query = request.args.get("query")
    limit = request.args.get("limit", 10, type=int)
    filters = {"pageSize": limit}
    try:
        result = curseforgeApi.search(query, filters)
        return jsonify(result)
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500

@app.route("/curseforge/mod/<modId>", methods=["GET"])
def curseforgeModDetails(modId):
    try:
        result = curseforgeApi.getMod(modId)
        return jsonify(result)
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500

@app.route("/curseforge/mod/<modId>/versions", methods=["GET"])
def curseforgeModVersions(modId):
    try:
        result = curseforgeApi.getModVersions(modId)
        return jsonify(result)
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500

@app.route("/curseforge/mod/<modId>/files/<fileId>", methods=["GET"])
def curseforgeVersionFiles(modId, fileId):
    try:
        result = curseforgeApi.getVersionFiles(modId, fileId)
        return jsonify(result)
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
