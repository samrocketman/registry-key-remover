"""
    Main driver for application
    Author: Corey Fournier
"""
from EntryList.RegShotListReader import RegShotListReader
from WindowsRegistry.WindowsRegistry import WindowsRegistry
from WindowsRegistry.WindowsRegistry import RegistryKey
from WindowsRegistry.WindowsRegistry import WindowsRegistryException
from SwitchParser import *
import sys


TAB = "\t"
NEW_LINE = "\n"
FILE_NAME_ARGUMENT_POSITION = 1

sp = SwitchParser(sys.argv)

registryInterface = WindowsRegistry()
registryList = RegShotListReader(sp.fileName)

if sp.deleteWithCascade :
    print "Deleting all keys with cascade\n"
    for line in registryList.getKeys():
        print TAB + "Removing: " + line
        keyInstance = RegistryKey(line.strip())
        try:
            registryInterface.removeKeyCascade(keyInstance)
            pass        
        except WindowsRegistryException, e:
            print e


print "Processing all keys\n"
for line in registryList.getKeys():
    print TAB + "Removing: " + line
    keyInstance = RegistryKey(line.strip())
    try:
        registryInterface.removeKey(keyInstance)
        #pass
    except WindowsRegistryException, e:
        print e

print NEW_LINE
print "Processing all values\n"

for line in registryList.getValues():
    print TAB + "Removing: " + line
    keyInstance = RegistryKey(line.strip())
    try:
        registryInterface.removeValue(keyInstance)
        #pass
    except WindowsRegistryException, e:
        print e
   
print NEW_LINE    
print "All done, Thanks for using Corey And Mike's Registry Reverter"
print NEW_LINE


