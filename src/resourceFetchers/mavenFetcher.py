import os
import requests

class MavenFetcher:
    # Public properties
    # These are useful outside of this class.
    fileName = ""
    pathStructure = ""
    resourceString = ""
    finalUrl = ""
    rootDir = ""

    # Private properties
    # These are not necessary outside of this class.
    __g = ""
    __a = ""
    __v = ""

    def __init__(self, baseUrl) -> None:
        # Handles trailing forward slash
        # insertion when there's none.
        if baseUrl[-1] != "/":
            baseUrl.insert(0, "/")
        self.targetUrl = baseUrl

    def fromString(self, inputString):
        inputString = inputString.split(":")

        self.__g = inputString[0]
        self.__a = inputString[1]
        self.__v = inputString[2]
        return self.__constructData()

    def fromGav(self, groupID, artifactID, artifactVersion):
        self.__g = groupID
        self.__a = artifactID
        self.__v = artifactVersion
        return self.__constructData()

    def __constructData(self):
        self.fileName = self.__a + "-" + self.__v + ".jar"
        self.pathStructure = self.__g.replace(".", "/") + "/" + self.__a + "/" + self.__v
        self.resourceString = self.pathStructure + "/" + self.fileName
        self.finalUrl = self.targetUrl + self.resourceString
        return self
    
    def setRoot(self, root):
        if root[-1] != "/":
            root = root + "/"
        self.rootDir = root
        return self

    def getResource(self) -> None:
        # Making sure there's no nonsense.
        if self.__g == "" or self.__a == "" or self.__v == "":
            raise Exception("Incomplete constructor. Please call the method fromString() or fromGav() before calling this method.")

        # Performing test to make sure we are looking at a JAR file.
        header = requests.head(self.finalUrl, allow_redirects=True)
        header.raise_for_status()
        header = header.headers.get('content-type')
        if "application/java-archive" in header.lower():
            try:
                response = requests.get(self.finalUrl, allow_redirects=True)
                response.raise_for_status()
                os.makedirs(self.rootDir + self.pathStructure, exist_ok=True)
                open(self.rootDir + self.resourceString, "wb").write(response.content)
            except Exception as e:
                raise Exception(f"An error occurred while obtaining the following resource:\n{e}")
        else:
            raise Exception("Failure in obtaining JAR. The requested link does not point to a JAR file.")