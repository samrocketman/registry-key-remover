import os
import re

class RegShotListReader:
    VALUES_ADDED_EXPRESSION = "Values added"
    KEYS_ADDED_EXPRESSION = "Keys added"
    REGULAR_EXPRESSION =  "\:[0-9]{0,3}(.)+\n(.)+(.|\s|\n)*?[-]{33}"
    def __init__(self, fileName):
        self.fileName = fileName
        f = open(self.fileName,'r')
        p = re.compile(VALUES_ADDED_EXPRESSION + REGULAR_EXPRESSION)
        m = p.search(f.read())
        if m:
            print 'Match found: ', m.group()
        else:
            print 'No match'

    def __getitem__(self,key):
        
        return f
        
    def getItem(self):
        #print "lenght=" + self.fileHandle.length
        print "lenght=%i" % 5