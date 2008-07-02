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
    HEADERS_TO_REMOVE = 2
    TAIL_TO_REMOVE = 1
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
        self.valuesArray = self.valuesArray[self.HEADERS_TO_REMOVE : len(self.valuesArray) - self.HEADERS_TO_REMOVE - self.TAIL_TO_REMOVE]
        
        self.keysArray = self.keysArray[self.HEADERS_TO_REMOVE : len(self.keysArray) - self.HEADERS_TO_REMOVE - self.TAIL_TO_REMOVE]
        
    """Gets all keys"""
    def getKeys(self):
        return self.keysArray
        pass
    
    """Gets all values"""
    def getValues(self):
        return self.valuesArray
        pass        