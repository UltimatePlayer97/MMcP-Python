import shutil
import requests
from mmcp import *
from concurrent.futures import ThreadPoolExecutor

class McFileDownloader:
     def fetchVersionManifest(self):
        # Fetch the version manifest from Mojang's servers
        manifest_url = "https://launchermeta.mojang.com/mc/game/version_manifest_v2.json"
        response = requests.get(manifest_url)
        manifest = response.json()
        return manifest
     
        # Fetch the Minecraft version manifest
        manifest = self.fetchVersionManifest()

     def getVersionInfo(self, version_id, manifest):
        # Get the specific version information from the manifest
        for version in manifest['versions']:
            if version['id'] == version_id:
                return version
        return None

     def downloadFile(self, url, dest):
            # Download a file from a given URL and save it to the destination
            try:
                response = requests.get(url, stream=True)
                dest.parent.mkdir(parents=True, exist_ok=True)
                with open(dest, 'wb') as f:
                    shutil.copyfileobj(response.raw, f)
                print(f"Downloaded: {url}")
            except Exception as e:
                print(f"Failed to download {url}: {e}")

     def downloadMinecraftFiles(self, version_info, instanceDir):
            # Download the necessary Minecraft files (JAR, libraries, and assets)
            version_data_url = version_info['url']
            version_data = requests.get(version_data_url).json()

            # Create necessary folders
            bin_dir = instanceDir / "bin"
            lib_dir = instanceDir / "libraries"
            assets_dir = instanceDir / "assets"

            bin_dir.mkdir(parents=True, exist_ok=True)
            lib_dir.mkdir(parents=True, exist_ok=True)
            assets_dir.mkdir(parents=True, exist_ok=True)

            # Download Minecraft JAR file
            jar_url = version_data['downloads']['client']['url']
            jar_dest = bin_dir / f"{version_info['id']}.jar"
            self.downloadFile(jar_url, jar_dest)

            # Download libraries
            # Function to download libraries and assets in parallel
            def download_libraries_and_assets():
                with ThreadPoolExecutor(max_workers=10) as executor:
                    # Download libraries
                    futures = []
                    for library in version_data['libraries']:
                        if 'downloads' in library and 'artifact' in library['downloads']:
                            lib_url = library['downloads']['artifact']['url']
                            lib_path = library['downloads']['artifact']['path']
                            lib_dest = lib_dir / lib_path
                            futures.append(executor.submit(self.downloadFile, lib_url, lib_dest))

                    # Download assets
                    asset_index_url = version_data['assetIndex']['url']
                    asset_index_dest = assets_dir / f"{version_info['id']}_assets.json"
                    self.downloadFile(asset_index_url, asset_index_dest)

                    # Wait for all downloads to finish
                    for future in futures:
                        future.result()