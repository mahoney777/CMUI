import wmi

c = wmi.WMI()

class CPU():


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


class UPDATES():
