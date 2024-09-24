import os
from mmcp import *
from tui import *



def main():
    print("MMcP - Make Minecraft Portable")

    if os.name == "nt": # Windows
        launcherDir = "C:\\XboxGames\\Minecraft Launcher\\Content\\Minecraft.exe"
    elif os.name == "posix": # Linux
        launcherDir = "minecraft-launcher"
    elif os.name == "darwin": #MacOS
        launcherDir = "/Applications/Minecraft.app"
    else:
        print("MMcP does not yet support your platform, stay tuned for more info.")
        return

    if Path(launcherDir).exists():
        minecraft = launcherDir
        mmcp = MMcP(minecraft)
        tui(mmcp)
    else:
        print("There was an issue picking up the launcher. MMcP does not implement a function to auto install.")
        print("Please download Minecraft Launcher at https://www.minecraft.net/en-us/download")
        return
    

if __name__ == "__main__":
    main()
    input()