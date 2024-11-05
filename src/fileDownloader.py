import shutil
import requests
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class McFileDownloader:
    def __init__(self):
        self.manifest = ""

    def fetchVersionManifest(self):
        # Fetch the version manifest from Mojang's servers
        manifest_url = "https://launchermeta.mojang.com/mc/game/version_manifest_v2.json"
        try:
            response = requests.get(manifest_url)
            response.raise_for_status()
            self.manifest = response.json()
            return self.manifest
        except requests.RequestException as e:
            logging.error(f"Failed to fetch version manifest: {e}")
            return None

    def getVersionInfo(self, version_id):
        # Get the specific version information from the manifest
        if not self.manifest:
            logging.error("Manifest is empty. Fetch the manifest first.")
            return None

        for version in self.manifest['versions']:
            if version['id'] == version_id:
                return version
        logging.warning(f"Version {version_id} not found in manifest.")
        return None

    def downloadFile(self, url, dest):
        # Download a file from a given URL and save it to the destination
        try:
            response = requests.get(url, stream=True)
            response.raise_for_status()
            dest.parent.mkdir(parents=True, exist_ok=True)
            with open(dest, 'wb') as f:
                shutil.copyfileobj(response.raw, f)
            logging.info(f"Downloaded: {url}")
        except requests.RequestException as e:
            logging.error(f"Failed to download {url}: {e}")

    def downloadMinecraftFiles(self, version_info, instanceDir):
        # Download the necessary Minecraft files (JAR, libraries, and assets)
        try:
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

            # Function to download libraries and assets in parallel
            def download_libraries_and_assets():
                with ThreadPoolExecutor(max_workers=10) as executor:
                    futures = []

                    # Download libraries
                    for library in version_data['libraries']:
                        if 'downloads' in library and 'artifact' in library['downloads']:
                            lib_url = library['downloads']['artifact']['url']
                            lib_path = Path(library['downloads']['artifact']['path'])
                            lib_dest = lib_dir / lib_path
                            futures.append(executor.submit(self.downloadFile, lib_url, lib_dest))

                    # Download assets
                    asset_index_url = version_data['assetIndex']['url']
                    asset_index_dest = assets_dir / f"{version_info['id']}_assets.json"
                    futures.append(executor.submit(self.downloadFile, asset_index_url, asset_index_dest))

                    # Wait for all downloads to finish
                    for future in futures:
                        future.result()

            download_libraries_and_assets()

        except requests.RequestException as e:
            logging.error(f"Failed to download Minecraft files: {e}")

# Example usage
if __name__ == "__main__":
    downloader = McFileDownloader()
    manifest = downloader.fetchVersionManifest()
    if manifest:
        version_info = downloader.getVersionInfo("1.16.5")
        if version_info:
            downloader.downloadMinecraftFiles(version_info, Path("/path/to/instanceDir"))