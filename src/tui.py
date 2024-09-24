import os
import time
import shutil
from mmcp import *

def tui(mmcp):
    while True:
        time.sleep(3)
        print("\nSelect an option:")
        print("[C] Create Instance")
        print("[L] List Instances")
        print("[Z] Compress an instance into a ZIP file")
        print("[D] Delete Instance")
        print("[S] Start Minecraft Launcher")
        print("[0] Exit MMcP")

        choice = input().upper()

        if choice == "C":
            name = input("Enter instance name: ")
            mmcp.createInstance(name)
        elif choice == "L":
            mmcp.listInstances()
        elif choice == "Z":
            name = input("Enter name of instance to compress: ")
            mmcp.compressInstance(name)
        elif choice == "D":
            name = input("Enter instance name to delete: ")
            mmcp.deleteInstance(name)
        elif choice == "S":
            mmcp.startMinecraft()
        elif choice == "0":
            print("Thank you for using MMcP")
            break
        else:
            print("Invalid input, please try again.")
        