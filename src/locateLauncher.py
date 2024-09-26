import platform
from pathlib import Path

class locateLauncher():
    __pathWindows = "C:\\XboxGames\\Minecraft Launcher\\Content\\Minecraft.exe"
    __pathLinux = "/sbin/minecraft-launcher" # Arch and its derivative
    __pathMacOS = "/Application/Minecraft.app"

    def __init__(self):
        self.__platform = platform.platform()

    def isWindows(self) -> bool:
        return self.__platform.startswith("Windows")

    def isLinux(self) -> bool:
        return self.__platform.startswith("Linux")

    def isMacOS(self) -> bool:
        return self.__platform.startswith("Mac")

    def getPathToLauncher(self) -> str | None:
        if self.isWindows() and Path(self.__pathWindows).exists():
            return self.__pathWindows
        elif self.isLinux() and Path(self.__pathLinux).exists():
            return self.__pathLinux
        elif self.isMacOS() and Path(self.__pathMacOS).exists():
            return self.__pathMacOS
        else:
            return None