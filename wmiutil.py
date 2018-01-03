import wmi
from socket import *

class Connector():

    def __init__(self, ip, username, password):
        self.ip = ip
        self.username = username
        self.password = password


    def connect(self, ip, username, password):
        try:
            print("Establishing connection to %s" % ip)
            c = wmi.WMI(ip, user=username, password=password)
            print("Connection established")
        except wmi.x_wmi:
            print("Your Username and Password of " + getfqdn(ip) + " are wrong.")


#p = Connector("192.168.31.83", "samAd", "Admin2017")
#p.connect("192.168.31.83", "samAd", "Admin2017")

class CPU():
    print()

class HDD():
    #Works out the Drive mapping, free space and total space of the Drive.
    #need to add connection to other PCs
    def __init__(self, drive, freespace, totalspace):
        self.drive = drive
        self.freespace = freespace
        self.totalspace = totalspace

    def diskspace(self):
        for d in c.Win32_LogicalDisk():
            a = d.FreeSpace
            a = int(a) / 2 ** 30
            freespace = round(a, 2)
            b = d.Size
            b = int(b) / 2 ** 30
            totalspace = round(b, 2)
            drive = d.Caption
            return drive, freespace, totalspace



class RAM():
    print()


class UPDATES():
    print()

def comd():
    ip = "192.168.31.83"
    username = r"192.168.31.83\samAd"
    password = "Admin2017"
    try:
        print("Establishing connection to %s" % ip)
        connection = wmi.WMI(ip, user=username, password=password)
        print("Connection established")
    except wmi.x_wmi:
        print("Your Username and Password of " + getfqdn(ip) + " are wrong.")


def basic():
    c = wmi.WMI("192.168.31.83", user="samAd", password="Admin2017")
    for disk in c.Win32_LogicalDisk(DriveType=3):
        print(disk)

basic()