import shutil
import requests
import subprocess
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor

class GameInstance:
    def __init__(self, instanceName, instanceDir):
        self.instanceName = instanceName
        self.instanceDir = instanceDir

class MMcP:
    def __init__(self, minecraftLauncher):
        self.minecraftLauncher = minecraftLauncher
        self.instances = []
        self.defaultDir = Path(__file__).resolve().parent.parent / "MMcP-Instances"

        # Create default directory for storing the instance
        if not self.defaultDir.exists():
            self.defaultDir.mkdir()
            print(f"Default instance created at: {self.defaultDir}")

    def fetchVersionManifest(self):
        # Fetch the version manifest from Mojang's servers
        manifest_url = "https://launchermeta.mojang.com/mc/game/version_manifest_v2.json"
        response = requests.get(manifest_url)
        manifest = response.json()
        return manifest

    def getVersionInfo(self, version_id, manifest):
        # Get the specific version information from the manifest
        for version in manifest['versions']:
            if version['id'] == version_id:
                return version
        return None

    def downloadFile(self, url, dest):
        # Download a file from a given URL and save it to the destination
        response = requests.get(url, stream=True)
        with open(dest, 'wb') as f:
            shutil.copyfileobj(response.raw, f)
        print(f"Downloaded: {url}")

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

    def createInstance(self, name):
        # Fetch the Minecraft version manifest
        manifest = self.fetchVersionManifest()

        # List available versions and prompt user to choose
        print("Available Minecraft Versions:")
        for version in manifest['versions']:
            print(f"- {version['id']}")

        version_id = input("Enter the Minecraft version: ")

        # Fetch version info for the selected version
        version_info = self.getVersionInfo(version_id, manifest)
        if not version_info:
            print(f"Version {version_id} not found!")
            return

        # Create instance directory
        instanceDir = self.defaultDir / name
        if not instanceDir.exists():
            instanceDir.mkdir()
            print(f"Instance created at: {instanceDir}")

        # Download the necessary files for the selected Minecraft version
        self.downloadMinecraftFiles(version_info, instanceDir)

        # Store the instance in memory
        instance = GameInstance(name, str(instanceDir))
        self.instances.append(instance)
        print(f"Created instance: {name}, with Minecraft version: {version_id}")
    
    def listInstances(self):
        if not self.defaultDir.exists() or not any(self.defaultDir.iterdir()):
            print("No instance found")
            print("Using Vanilla instance.")
        else:
            print("Game instances: ")
            # Iterate over the directories in the default directory
            for instanceDir in self.defaultDir.iterdir():
                if instanceDir.is_dir():
                    print(f" - {instanceDir.name} (Directory: {instanceDir})")

    def deleteInstance(self, name):
        instanceDir = self.defaultDir / name
        
        if instanceDir.exists() and instanceDir.is_dir():
            # Remove the folder from the file system
            shutil.rmtree(instanceDir)
            print(f"Deleted instance directory: {instanceDir}")
            
            # Remove the instance from the memory list, if it exists
            instanceToRemove = next((i for i in self.instances if i.instanceName == name), None)
            if instanceToRemove:
                self.instances.remove(instanceToRemove)
        else:
            print(f"No instance directory found for: {name}")

    def startMinecraft(self):
        print("Starting Minecraft Launcher, please wait.....")
        subprocess.Popen(self.minecraftLauncher)