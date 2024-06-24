# pip install speedtest-cli
import speedtest

class Speed():
    def __init__(self):
        # mbps unit
        self.speed = 100.0
        self.__tester__ = speedtest.Speedtest(secure=True)

    def getBestServer(self):
        try:
            info = self.__tester__.get_best_server()
            country, name = info['country'], info['name']
            return country, name
        except Exception as e:
            print(e)
            return "", ""

    def testDown(self):
        self.speed = self.__tester__.download() / (10 ** 6)
        print(f"{self.speed} Mbps")
        return self.speed