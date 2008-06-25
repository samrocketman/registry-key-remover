class RegShotListReader(IEntryType):
    def __getitem__(self,key):
        if os.path.isfile(filename):
            f = os.open(filename,'r')
            return f            
        else :
            print "cant find the file"
