import wifi
import math
import time
import os
import netifaces
from wireless import Wireless
from collections import OrderedDict


class Connector():

    def __init__(self):
        self.interface = "wlan1"
        self.wifilist = []
        self.ratings = OrderedDict()
        #blacklist
        self.blacklist = []
        self.blacklistFile = "./blacklist.txt"
        #passwords
        self.passwords = {}
        self.passwordsFile = "./passwords.txt"
        #cell object
        self.cells = None
        self.wifiConfigFile = "/etc/wpa_supplicant/wpa_supplicant.conf"
        #wpa connector object
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
        #sort dictionary by values.
        values = sorted(dict1.values(), reverse=True)
        print("values")
        print(values)
        newdict = OrderedDict()
        for val1 in values:
            for key, value in dict1.items():
                if value == val1:
                    newdict[key] = value
        return newdict

    def scan(self):
        #find available wireless networks
        try:
            for cell in self.search():
                self.ratings[str(cell.ssid)] = self.rate(cell)
            time.sleep(4)
            print(self.ratings)
        except:
            print("couldn't can networks")
        try:
            for cell in self.search():
                self.ratings[str(cell.ssid)] = self.rate(cell)
            time.sleep(4)
            print(self.ratings)
        except:
            print("couldn't can networks")
        try:
            for cell in self.search():
                self.ratings[str(cell.ssid)] = self.rate(cell)
            print(self.ratings)
        except:
            print("couldn't can networks")
        for ssid in self.blacklist:
            self.ratings.pop(ssid, None)
        self.ratings = self.sortDict(self.ratings)
        return self.ratings

    def ipExists(self):
        try:
            test = netifaces.ifaddresses(c.interface)[2]
            return True
        except:
            return False

    def conn(self, ssid):
        #if not connected to a wifi already:
        if self.wireless.current() == None or not self.ipExists():
            #flush both essid and ip
            os.system('sudo iwconfig ' + self.interface + ' essid ""')
            time.sleep(3)
            os.system('ip addr flush dev wlan1')
            time.sleep(4)
	    for cell in self.cells:
	        if cell.ssid == ssid:
	            print("connecting to: " + str(ssid))
                    #connect to insecure wifi
	            if cell.encrypted is False:
	                try:
	                    print("\nconnecting to open wifi")

                            f = open(self.wifiConfigFile, 'r')
                            lines = f.readlines()
                            ssidExists = False
                            for line in lines:
                                if 'ssid="' + str(ssid) in line:
                                    ssidExists = True
                            f.close()
                            if not ssidExists:
                                cmd = "network={\n" + 'ssid="' + str(ssid) + '"\n' + "key_mgmt=NONE\n" + "}\n"
                                f = open(self.wifiConfigFile, 'a')
                                f.write(cmd)
                                f.close()
                            cmd = "sudo service wpa_supplicant restart"
                            os.system(cmd)
                            time.sleep(3)
                            if "'" in cell.ssid:
                                cmd = "sudo iwconfig " + self.interface + ' essid "' + str(cell.ssid) + '"'
                            else:
                                cmd = "sudo iwconfig " + self.interface + " essid '" + str(cell.ssid) + "'"
                            os.system(cmd)
                            #if connected and acquired an ip address
                            if self.wireless.current() is not None:
                                for num in range(0, 3):
                                    if self.ipExists():
                                        return True
                                    time.sleep(30)
                                print("couldn't connect")
                                return False
                            else:
                                print("couldn't connect1")
                                return False
	                except:
                            print("couldn't connect2")
	                    return False
                    #connect to encrypted wireless networks
	            elif cell.encrypted is True:
	                print("encrypted, looking for PW")
	                try:
	                    pw = self.passwords[ssid]
	                    print(pw)
	                    self.wireless.connect(ssid, pw)
                            return True
	                except:
	                    print("couldn't connect'")
	                    return False
        else:
            print("already connected to: " + str(self.wireless.current()))
            return self.wireless.current()

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

    def sigmoid(self, x):
        return 1 / (1 + math.exp(-x))


#setup
c = Connector()
c.readBlacklist()
c.readPW()

#get quality of each available network
print(c.scan())

#make best connection
c.makeConnection()
