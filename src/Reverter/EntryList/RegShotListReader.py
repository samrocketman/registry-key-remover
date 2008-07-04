"""
Reads the contents of the RegShot comparison file and parses out 
the Values and Keys Added.

Author: Corey Fournier
"""
import os
import re

class RegShotListReader:
    VALUES_ADDED = "Values added"
    KEYS_ADDED = "Keys added"
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
        
        self.valuesArray = []
        
        #Put the values into an array
        self.keysArray = keysAdded.split(self.NEW_LINE)
        self.valuesArray = valuesAdded.split(self.NEW_LINE)
        
                
        #Get rid of the headers and the tail
        self.valuesArray = self.valuesArray[self.HEADER_LINES_TO_REMOVE : len(self.valuesArray) - self.TAIL_LINES_TO_REMOVE]
        
        self.keysArray = self.keysArray[self.HEADER_LINES_TO_REMOVE : len(self.keysArray) - self.TAIL_LINES_TO_REMOVE]
        
        for line in self.keysArray:
            print line + self.NEW_LINE
        
        
    def getKeys(self):
        """Gets all keys
            Returns an array of Registry Keys as a string
        """
        return self.keysArray
    
    def getValues(self):
        """Gets all values
            Returns an array of Registry Values as a string
        """
        return self.valuesArray