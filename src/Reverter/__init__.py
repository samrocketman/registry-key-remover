#Main driver for application
#@author: Corey Fournier


filename = "/home/corey/workspace/HelloWorld/InstallRemove.txt"
et = EntryList.RegShotListReader(fileName)
for line in et:
        print line 