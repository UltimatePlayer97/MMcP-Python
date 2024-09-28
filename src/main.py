import os
from mmcp import *
from tui import *
from locateLauncher import *


def main():
    tui = TUI()
    print("MMcP - Make Minecraft Portable")

    launcherDir = locateLauncher().getPathToLauncher()
    if launcherDir == None:
        print("An issue occurred while parsing launcher location. Either your platform is unsupported, or the path to the launcher doesn't exist.\n")
        print("If you're on a supported platform but doesn't have the launcher installed, you can download and install the launcher from")
        print("https://www.minecraft.net/en-us/download")
        exit()
    else:
        minecraft = launcherDir
        mmcp = MMcP(minecraft)
        tui.mainMenu(mmcp)


if __name__ == "__main__":
    main()
    #input()