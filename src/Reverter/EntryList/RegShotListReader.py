import os

class RegShotListReader:
    def __init__(self, fileName):
        self.fileName = fileName

    def __getitem__(self,key):
        f=open(self.fileName,'r')
        return f
        
    def getItem(self):
        #print "lenght=" + self.fileHandle.length
        print "lenght=%i" % 5