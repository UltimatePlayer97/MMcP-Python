import os
import shutil
import subprocess
from pathlib import Path

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

    def createInstance(self, name):
        minecraftVersion = input("Enter the Minecraft version: ")

        # Use the default directory to store the instance
        instanceDir = self.defaultDir / name
        if not instanceDir.exists():
            instanceDir.mkdir()
            print(f"Instance created at: {instanceDir}")

        # Create and store the new instance in memory
        instance = GameInstance(name, str(instanceDir))
        self.instances.append(instance)
        print(f"Created instance: {name}, in the directory: {instanceDir}")
    
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