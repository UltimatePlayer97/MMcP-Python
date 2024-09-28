import os
import time
import shutil
from mmcp import *

class TUI:
    __clearLine = "\033[H\033[1J"       # Clears a whole line
    __clearConsole = "\033[H\033[2J"    # Clears entire console
    __clearAll = "\033[H\033[3J"        # Clears entire console PLUS scrollback buffer (NUCLEAR!!!)

    def clear(self, mode = 0):
        if mode == 1:
            print(self.__clearLine, end='')
        elif mode == -1:
            print(self.__clearAll, end='')
        else:
            print(self.__clearConsole, end='')

    def mainMenu(self, mmcp):
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
        