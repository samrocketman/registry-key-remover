"""This file contains a class that parses the arguments passed into the application.
    It checks for valid input and sets public variables to the values given input.
Author: Corey Fournier
"""
class SwitchParser:
    """
    F - file
    C - cascade
    """
    SWITCHES = ["F","C"]
    """File name of file passed in"""
    fileName = None
    """Delete with cascade is enabled if true/ false otherwise"""
    deleteWithCascade = False    
    
    """ Class constructor
        commandLineArguments - Arguments passed in at the command line
    """
    def __init__(self, commandLineArguments):
        arguments = []
        switch = None
        argument = None
        
        if len(commandLineArguments) == 1:
            print "You must provide arguments EX:"
            print "-" + self.SWITCHES[0] + " filename (regshot keys)"
            print "-" + self.SWITCHES[1] + " (delete with cascade)"
        
        """Clean the arguments up"""        
        for argument in commandLineArguments:
            if argument != "" :
                argument = argument.strip()
            if argument != "" :
                arguments.append(argument)
        """Now look at all of the arguments to see if any match"""
        for i in range(len(arguments)):
            argument = arguments[i]
            #see if the current argument is a switch indicator
            if argument.find("-",0,1)  > -1 :
                switch = argument.upper()[1:2]
                if self.SWITCHES.count(switch) > 0 :
                    if self.SWITCHES[0] == switch: #The next argument is a file
                        argument = arguments[i + 1]
                        self.fileName = argument 
                    elif self.SWITCHES[1] == switch: # Delete with cascade is selected
                        self.deleteWithCascade = True
        
        if self.fileName == None :
            print "File name as an argument is required with the flag -" + self.SWITCHES[0] + NEW_LINE
            exit()