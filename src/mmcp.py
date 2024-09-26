import os
import shutil
import subprocess
from pathlib import Path
from fileDownloader import *

class GameInstance:
    def __init__(self, instanceName, instanceDir):
        self.instanceName = instanceName
        self.instanceDir = instanceDir

class MMcP(McFileDownloader):
    def __init__(self, minecraftLauncher):
        self.manifest = super().fetchVersionManifest()
        self.minecraftLauncher = minecraftLauncher
        self.instances = []
        self.defaultDir = Path(__file__).resolve().parent.parent / "MMcP-Instances"

        # Create default directory for storing the instance
        if not self.defaultDir.exists():
            self.defaultDir.mkdir()
            print(f"Default instance created at: {self.defaultDir}")

        else:
            for i in Path(self.defaultDir).iterdir():
                self.instances.append(GameInstance(i.name, i))
                print("Imported instance:\n{} | {}".format(i.name,i))

    def createInstance(self, name):

        # Ask user what type of versions they want to see
        print("\nSelect which versions to show:")
        print("[1] Releases only")
        print("[2] Releases and Snapshots")
        print("[3] Include all (Releases, Snapshots, Betas, Alphas)")

        choice = input("Choose which channels you wish to see: ")

        # Filter versions based on user choice
        if choice == "1":
            version_types = ["release"]
        elif choice == "2":
            version_types = ["release", "snapshot"]
        elif choice == "3":
            version_types = ["release", "snapshot", "old_beta", "old_alpha"]
        else:
            print("Invalid choice. Defaulting to Releases only.")
            version_types = ["release"]

        # List available versions and prompt user to choose
        filtered_versions = [v for v in self.manifest['versions'] if v['type'] in version_types]
        print("\nAvailable Minecraft Versions:")
        for version in filtered_versions:
            print(f"- {version['id']} ({version['type']})")

        version_id = input("Enter the Minecraft version: ")

        # Fetch version info for the selected version
        version_info = self.getVersionInfo(version_id, self.manifest)
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
    
    def compressInstance(self, name):
            instancePath = os.path.join("MMcP-Instances", name)
            zipPath = os.path.join("MMcP-Instances", name)
            shutil.make_archive(zipPath, "zip", instancePath)
            print(f"Instance '{name}' has been compressed into '{zipPath}.zip'")

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
        i = 0
        print("Select instance to run:")
        for j in self.instances:
            i += 1
            print("[{}]: {}".format(i, j.instanceName))
        
        try:
            selected = int(input()) - 1
        except:
            print("Input is not a number. Defaulting to first option.")
            selected = 0
        
        print("Starting Minecraft Launcher, please wait.....")
        formattedString = "--workDir=" + str(self.instances[selected].instanceDir.absolute())
        subprocess.Popen([self.minecraftLauncher, formattedString])