import wmi

c = wmi.WMI()

class Harddrive:


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


if __name__ == "__main__":
    hdd = Harddrive(None, None, None)








