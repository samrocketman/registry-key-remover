#Fake python interface
#This is only a stub for all other Enty handlers
#@author: Corey Fournier

class IEntryType:
    #@param fileName: Set the name of the files to be parsed 
    def __init__(self,fileName):
        self.fileName = fileName
        pass
    
    def __getitem__(self,key):
        pass
