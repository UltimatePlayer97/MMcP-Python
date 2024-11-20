import requests

class MavenFetcher:
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
        return self

    def fromGav(self, groupID, artifactID, artifactVersion):
        self.__g = groupID
        self.__a = artifactID
        self.__v = artifactVersion
        return self

    def getResource(self) -> None:
        # Making sure there's no nonsense.
        if self.__g == "" or self.__a == "" or self.__v == "":
            raise Exception("Incomplete constructor. Please call the method fromString() or fromGav() before calling this method.")

        # Assembles everything to become a downloadable URL.
        self.__g = self.__g.replace(".", "/")
        self.__n = self.__a + "-" + self.__v + ".jar"
        self.__s = self.__g + "/" + self.__a + "/" + self.__v + "/" + self.__n

        self.__u = self.targetUrl + self.__s

        # Performing test to make sure we are looking at a JAR file.
        header = requests.head(self.__u, allow_redirects=True)
        header.raise_for_status()
        header = header.headers.get('content-type')
        if "application/java-archive" in header.lower():
            try:
                response = requests.get(self.__u, allow_redirects=True)
                response.raise_for_status()
                open(self.__n, "wb").write(response.content)
            except Exception as e:
                raise print(f"An error occurred while obtaining the following resource:\n{e}")
        else:
            raise Exception("Failure in obtaining JAR. The requested link does not point to a JAR file.")