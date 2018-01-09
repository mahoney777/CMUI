import win32com.client
import win32con
import win32api
import pywintypes
import re
import wmi

def get_software_updates(update_seeker, installed):
    c = wmi.WMI()
    # Search installed/not installed Software Windows Updates
    search_string = "IsInstalled=%d and Type='Software'" % installed
    search_update = update_seeker.Search(search_string)
    _ = c.client.Dispatch("Microsoft.Update.UpdateColl")
    updates = []
    categories = []
    update_dict = {}
    # compiles the regex pattern for finding Windows Update codes
    updates_pattern = re.compile(r'KB+\d+')
    for update in search_update.Updates:
        update_str = str(update)
        # extracts Windows Update code using regex
        update_code = updates_pattern.findall(update_str)
        for category in update.Categories:
            category_name = category.Name
            print("[*] Name: " + update_str + " - " +
                  "url: " + "https://support.microsoft.com/en-us/kb/{}".format(
                "".join(update_code).strip("KB")) + " - " +
                  "Category: " + category_name)
            updates.append(update_str)
            categories.append(category_name)
    # converts lists to tuples in order to be used as a dictionary key
    hashable = tuple(updates)
    hashable_category = tuple(categories)
    # creates category:update dictionary
    for update in hashable:
        for category_update in hashable_category:
            update_dict[category_update] = str(update)
    return update_dict

def enum_winupdates():
    """
    ip = "192.168.31.2"
    username = "CMUIAdmin"
    password = "Admin2017"
    c = wmi.WMI(ip, user=username, password=password)
    """
    c = wmi.WMI()
    for os in c.Win32_OperatingSystem():
        print(os.Caption)
    wua = c.client.Dispatch("Microsoft.Update.Session")
    update_seeker = wua.CreateUpdateSearcher()
    print("\n[+] Enumerating available Windows or Drivers' Updates not installed...(if any)\n")
    available = get_software_updates(update_seeker, installed=False)
    return available

enum_winupdates()


