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
        self.defaultDir = Path(os.getcwd()) / "MMcP-Instances"

        # Create default directory for storing the instance
        if not self.defaultDir.exists():
            self.defaultDir.mkdir()
            print(f"Default instance created at: {self.defaultDir}")

    def createInstance(self, name, dir_):
        minecraftVersion = input("Enter the Minecraft version: ")

        if not dir_:
            newDir = self.defaultDir / name
            if not newDir.exists():
                newDir.mkdir()
                print(f"Instance created at: {newDir}")
            instanceDir = newDir
        else:
            instanceDir = Path(dir_)

        instance = GameInstance(name, str(instanceDir))
        self.instances.append(instance)
        print(f"Created instance: {name}, in the directory: {instanceDir}")
    
    def listInstances(self):
        if not self.instances:
            print("No instance found")
            print("Using Vanilla instance.")
        else:
            print("Game instances: ")
            for instance in self.instances:
                # Check if the directory exists
                if os.path.isdir(instance.instanceDir):
                    print(f" - {instance.instanceName} (Directory: {instance.instanceDir})")
                else:
                    print(f" - {instance.instanceName} (Directory: {instance.instanceDir}) - Directory not found!")
    
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
                print(f"Deleted instance: {name} from memory")
        else:
            print(f"No instance directory found for: {name}")

    def startMinecraft(self):
        print("Starting Minecraft Launcher, please wait.....")
        subprocess.Popen(self.minecraftLauncher)