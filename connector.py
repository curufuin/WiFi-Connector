import wifi
import math
import time
from wireless import Wireless
from collections import OrderedDict


class Connector():

    def __init__(self):
        self.interface = "wlan0"
        self.wifilist = []
        self.ratings = OrderedDict()
        #blacklist
        self.blacklist = []
        self.blacklistFile = "./blacklist.txt"
        #passwords
        self.passwords = {}
        self.passwordsFile = "./passwords.txt"
        #wifi objects
        self.cells = None
        self.wireless = Wireless()

    def search(self):
        self.cells = wifi.Cell.all(self.interface)
        for cell in self.cells:
            self.wifilist.append(cell)
        return self.wifilist

    def rate(self, cell):
        sig = 100 + cell.signal
        qual = c.sigmoid(float(eval(str(cell.quality) + ".0")))
        return sig * qual

    def sortDict(self, dict1):
        values = sorted(dict1.values())
        newdict = OrderedDict()
        for key,value in dict1.items():
            val1 = values.pop()
            if value == val1:
                newdict[key] = value
        return newdict

    def scan(self):
        for cell in self.search():
            self.ratings[str(cell.ssid)] = self.rate(cell)
        for ssid in self.blacklist:
            self.ratings.pop(ssid, None)
        self.ratings = self.sortDict(self.ratings)
        return self.ratings

    def conn(self, ssid):
        for cell in self.cells:
                if cell.ssid == ssid:
                    print("connecting to: " + str(ssid))
                    if cell.encrypted is False:
                        try:
                            print("connecting to open wifi")
                            return self.wireless.connect(ssid, "")
                        except:
                            print("couldn't connect")
                            return False

                    elif cell.encrypted is True:
                        print("encrypted, looking for PW")
                        try:
                            pw = self.passwords[ssid]
                            print(pw)
                            return self.wireless.connect(ssid, pw)
                        except:
                            print("couldn't connect'")
                            return False

    def makeConnection(self):
        #go through list of wifi SSID's by best connection and connect.
        connected = False
        for ssid, rating in self.ratings.items():
            connected = self.conn(ssid)
            time.sleep(5)
            if connected:
                print("connected")
                break




    def readBlacklist(self):
        with open(self.blacklistFile) as f:
            self.blacklist = f.read().splitlines()

    def readPW(self):
        with open(self.passwordsFile) as f:
            for line in f:
                key, val = line.split(":")
                self.passwords[key] = val.rstrip()
                print(self.passwords)

    def sigmoid(self, x):
        return 1 / (1 + math.exp(-x))


#setup
c = Connector()
c.readBlacklist()
c.readPW()


#get quality of network
print(c.scan())

#make best connection
c.makeConnection()
