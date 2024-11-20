import shutil
import requests
import json
from resourceFetchers.mavenFetcher import MavenFetcher
from concurrent.futures import ThreadPoolExecutor

class FabricMeta:
    __base_manifest_url = "https://meta.fabricmc.net/v2/versions"
    __manifest_url = __base_manifest_url + "/game"

    # Get the required data first.
    manifest = requests.get(__manifest_url)
    if (manifest.ok and manifest.status_code == 200):
        manifest = manifest.json()

    def __init__(self, compatible_version):
        self.compatible_version = compatible_version

    def fetch(self):
        newLink = self.__base_manifest_url + "/loader"
        data = "No resources available" # Will be modified if succeeded
        try:
            for i in self.manifest:
                if(i["version"] == self.compatible_version):
                    newResponse = requests.get(newLink + "/" + i["version"])
                    newResponse.raise_for_status()

                    # Gotta say, not a big fan of not having an equivalent of
                    # Javascript's Array.forEach() function in Python, so we got
                    # A bunch of for-in's just to get something similar working.
                    # This may be redundant, but we are defaulting to using the one
                    # that is marked as stable for convenience
                    for i in newResponse.json():
                        if i["loader"]["stable"]:
                            data = i
                            break
                    
                    print(f"Selected loader version {data["loader"]["version"]} as the best version.")

                    # While the idea is to programatically get the link to the main resource,
                    # I decided I've wasted enough time doing all that, so here it is.
                    mm = MavenFetcher("https://maven.fabricmc.net/")
                    mm.fromString(data["loader"]["maven"])
                    
                    # Yo dawg, I heard you guys love some loops.
                    # So here's something for you:
                    # 
                    # Loop Hell, trademark.
                    for i in data["launcherMeta"]["libraries"]:
                        for j in data["launcherMeta"]["libraries"][i]:
                            try:
                                mm = MavenFetcher(j["url"])
                                mm.fromString(j["name"])
                                print(f"fetched {j["name"]} from {j["url"]}")
                            except Exception as e:
                                print(f"Something happened, and here's the error:\n{e}")
                                break

                    break
        except Exception as e:
            print("Error occured while parsing data:\n",e)

        return data