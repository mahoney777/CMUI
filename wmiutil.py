import sys, wmi, os
from socket import *
import pythoncom
import threading

class Connector():
    """WMI Connector to server"""
    def __init__(self, ip, username, password):
        self.ip = ip
        self.username = username
        self.password = password

        pythoncom.CoInitialize()
        #Use ip,username,password to connect to server
        global c
        c = wmi.WMI()
        #c = wmi.WMI(ip, user=username, password=password)

    def connect(self):
        try:
            #print("Establishing connection to %s" % ip)
            for os in c.Win32_OperatingSystem():
                print(os.Caption)
                return os.Caption
            print("Connection established")
        except wmi.x_wmi:
            print("Your Username and Password of " + getfqdn(ip) + " are wrong.")
            print("error")


    def diskspace(self):
        for d in c.Win32_LogicalDisk():
            a = d.FreeSpace
            a = int(a) / 2 ** 30
            freespace = round(a, 2)
            b = d.Size
            b = int(b) / 2 ** 30
            totalspace = round(b, 2)
            drive = d.Caption
            print("The drive %s has %s GB free space out of its %s GB capacity" % (drive, freespace, totalspace))
            return drive, freespace, totalspace


    def get_uptime(self):
        uptime = int([uptime.SystemUpTime for uptime in c.Win32_PerfFormattedData_PerfOS_System()][0])
        uptimehours = uptime / 3600
        uptimedays = uptimehours / 24
        uptimedays = round(uptimedays, 2)
        print("The Server has been up for %d days" % (uptimedays))
        return uptimedays

    def get_cpu(self):
        cpuload = [cpu.LoadPercentage for cpu in c.Win32_Processor()]
        avgcpuload = int(sum(cpuload) / len(cpuload))  # avg all cores/processors! Change to per core?
        print("The CPU load is %d percent" % (avgcpuload))
        numofcores = ([cpu.NumberOfLogicalProcessors for cpu in c.Win32_ComputerSystem()][0])
        numofcpu = ([cpu.NumberOfProcessors for cpu in c.Win32_ComputerSystem()][0])
        cpu_name = ([cpu.Name for cpu in c.Win32_Processor()][0])
        return avgcpuload, numofcores, numofcpu, cpu_name


    def get_mem_mbytes(self):
        available_mbytes = int([mem.AvailableMBytes for mem in c.Win32_PerfFormattedData_PerfOS_Memory()][0])
        print("------------------------")
        print("Change to GB")
        print("The available RAM remaining in mbytes is %d" % (available_mbytes)) #Change to GB and add max mem and % useage?
        print("notinusemem already does this with my own code")
        print("------------------------")

    def get_mem_pct(self):
        pct_in_use = int([mem.PercentCommittedBytesInUse for mem in c.Win32_PerfFormattedData_PerfOS_Memory()][0])
        print("%d percent of RAM has been used" % (pct_in_use))

    def totaltestmem(self):
        memt = ([mem.TotalVisibleMemorySize for mem in c.Win32_OperatingSystem()][0])
        a = memt
        a = int(a) / 2 ** 20
        totalmem = round(a, 2)
        #This is my own code that returns the RAM. 7.9 on laptop is correct
        print("This server has %d GB of total RAM" % (totalmem))
        return totalmem

    def notinusemem(self):
        numem = ([mem.FreePhysicalMemory for mem in c.Win32_OperatingSystem()][0])
        a = numem
        a = int(a) / 2 ** 20
        notinuse = round(a, 2)
        print("%d GB of RAM is not in use" % (notinuse))
        return notinuse





    def sysinfo(self):
        #This uses the Win32 ComputerSystem Class
        vm = ([system.Model for system in c.Win32_ComputerSystem()][0])
        name = ([system.Name for system in c.Win32_ComputerSystem()][0])
        status = ([system.Status for system in c.Win32_ComputerSystem()][0])
        return vm, name, status







def servertest():
    p = Connector("192.168.31.2", "CMUIAdmin", "Admin2017")
    """p.connect()
    p.diskspace()
    p.get_uptime()
    p.get_cpu()
    p.totaltestmem()
    p.notinusemem()"""
    p.sysinfo()
    p.get_cpu()



