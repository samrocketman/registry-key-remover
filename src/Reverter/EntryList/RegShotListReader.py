"""
Reads the contents of the RegShot comparison file and parses out 
the Values and Keys Added.

Author: Corey Fournier
        Sam Gleske
"""
#import os (according to eclipse this is not needed)
import re

class RegShotListReader:
    """Values Added Header used in the regshot file"""
    VALUES_ADDED = "Values added"
    """Keys Added Header used in the regshot file"""
    KEYS_ADDED = "Keys added"
    """Files Added Header used in the regshot file"""
    FILES_ADDED = "Files added"
    """Folders Added Header used in the regshot file"""
    FOLDERS_ADDED = "Folders added"
    """Regular expression used to find the regshot keys or values"""
    REGULAR_EXPRESSION =  "\:[0-9]{0,4}(.)+\n(.)+(.|\s|\n)*?[-]{33}"
    HEADER_LINES_TO_REMOVE = 2
    TAIL_LINES_TO_REMOVE = 2
    NEW_LINE = "\n"
    
    """ Class contructor """
    def __init__(self, fileName):
        self.fileName = fileName
        
        #Get the contents of the file
        f = open(self.fileName,'r')
        #Load the contents into a temporary location
        fileContents = f.read()
        
        #Get all values added
        p = re.compile(self.VALUES_ADDED + self.REGULAR_EXPRESSION)
        m = p.search(fileContents)
        valuesAdded = m.group()
        
        #Get all keys added
        p = re.compile(self.KEYS_ADDED + self.REGULAR_EXPRESSION)
        m = p.search(fileContents)
        keysAdded = m.group()
        
        #Get all files added
        p = re.compile(self.FILES_ADDED + self.REGULAR_EXPRESSION)
        m = p.search(fileContents)
        filesAdded = m.group()
        
        #Get all folders added
        p = re.compile(self.FOLDERS_ADDED + self.REGULAR_EXPRESSION)
        m = p.search(fileContents)
        foldersAdded = m.group()
        
        self.valuesArray = []
        self.keysArray = []
        self.filesArray = []
        self.foldersArray = []
        
        #Put the values into an array (Python List)
        self.valuesArray = valuesAdded.split(self.NEW_LINE)
        self.keysArray = keysAdded.split(self.NEW_LINE)
        self.filesArray = filesAdded.split(self.NEW_LINE)
        self.foldersArray = foldersAdded.split(self.NEW_LINE)
                
        #Get rid of the headers and the tail
        self.valuesArray = self.valuesArray[self.HEADER_LINES_TO_REMOVE : len(self.valuesArray) - self.TAIL_LINES_TO_REMOVE]
        self.keysArray = self.keysArray[self.HEADER_LINES_TO_REMOVE : len(self.keysArray) - self.TAIL_LINES_TO_REMOVE]
        self.filesArray = self.filesArray[self.HEADER_LINES_TO_REMOVE : len(self.filesArray) - self.TAIL_LINES_TO_REMOVE]
        self.foldersArray = self.foldersArray[self.HEADER_LINES_TO_REMOVE : len(self.foldersArray) - self.TAIL_LINES_TO_REMOVE]
        
        # Unnecessary output
        #for line in self.keysArray:
        #    print line + self.NEW_LINE
        
    
    def getValues(self):
        """ Gets all values
            Returns an array of Registry Values as a string
        """
        return self.valuesArray
        
    def getKeys(self):
        """ Gets all keys
            Returns an array of Registry Keys as a string
        """
        return self.keysArray
    
    def getFiles(self):
        """ Gets all files
            Returns an array of file paths
        """
        return self.filesArray
    
    def getFolders(self):
        """ Gets all folders
            Returns an array of folder paths
        """
        return self.foldersArray