#Main driver for application
#@author: Corey Fournier

from EntryList.RegShotListReader import RegShotListReader

fileName = "/home/corey/workspace/HelloWorld/InstallRemove.txt"

el = RegShotListReader(fileName)

#el.getItem()
for line in el:
        print line 