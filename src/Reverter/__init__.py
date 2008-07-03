"""
    Main driver for application
    Author: Corey Fournier
"""
from EntryList.RegShotListReader import RegShotListReader
from WindowsRegistry.WindowsRegistry import WindowsRegistry
from WindowsRegistry.WindowsRegistry import RegistryKey
import sys

TAB = "\t"
NEW_LINE = "\n"
FILE_NAME_ARGUMENT_POSITION = 1

"""Check for the file name passed in"""
if sys.argv[FILE_NAME_ARGUMENT_POSITION] == "":
    print "File name as an argument is required" + NEW_LINE
    exit()
else :
    fileName = sys.argv[FILE_NAME_ARGUMENT_POSITION] 
    print "Using file '" + fileName + "'" + NEW_LINE

registryInterface = WindowsRegistry()
registryList = RegShotListReader(fileName)

print "Processing all keys\n"
for line in registryList.getKeys():
    print TAB + "Removing: " + line
    keyInstance = RegistryKey(line.strip())
    registryInterface.removeKey(keyInstance)

print NEW_LINE
print "Processing all values\n"

for line in registryList.getValues():
    print TAB + "Removing: " + line
    keyInstance = RegistryKey(line.strip())
    registryInterface.removeValue(keyInstance)
    
print NEW_LINE    
print "All done, Thanks for using Corey And Mike's Registry Reverter"
print NEW_LINE
