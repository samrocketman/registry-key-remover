"""
    Main driver for application
    Author: Corey Fournier
"""
from EntryList.RegShotListReader import RegShotListReader
from WindowsRegistry.WindowsRegistry import WindowsRegistry

TAB = "\t"
NEW_LINE = "\n"

fileName = "/home/corey/workspace/HelloWorld/InstallRemove.txt"

registryInterface = WindowsRegistry()
registryList = RegShotListReader(fileName)

print "Processing all keys\n"
for line in registryList.getKeys():
    print TAB + "Removing: " + line
    registryInterface.removeKey(line.strip())

print NEW_LINE
print "Processing all values\n"

for line in registryList.getValues():
    print TAB + "Removing: " + line
    registryInterface.removeValue(line.strip())
    print line
    
print NEW_LINE    
print "All done, Thanks for using Corey And Mike's Registry Reverter"
print NEW_LINE
