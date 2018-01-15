drivelist = [('C:', 236, 61), ('D:', 200, 10)]
wow = len(drivelist)
"""
for element in drivelist:
    for i in range(wow):
        print(element)
        print(i)
        print("----------------------------------------")
        mapping, freespace, totalspace = drivelist[i]
        print(mapping, freespace, totalspace)
        print("----------------------------------------")"""


for i in range(wow):
    print(i)
    print("----------------------------------------")
    mapping, freespace, totalspace = drivelist[i]
    print(mapping, freespace, totalspace)
    print("----------------------------------------")
















    for i in range(nameslen):
        print('-------------------')
        print(i)
        i = (names[i])
        print(i)
        serverid, name, ip, prole, srole, com, make = i
        print(serverid, name, prole, srole, com, make)
        while test == False:
            test = dict(id=serverid, name=name, ip=ip, prole=prole, srole=srole, com=com, make=make)
            print(test)
            print('--------------------')
        else:
            test.append(i)
            print(test)
            print("Sick")
            print("---------------------")