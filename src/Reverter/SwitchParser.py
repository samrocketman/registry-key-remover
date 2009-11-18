"""This file contains a class that parses the arguments passed into the application.
    It checks for valid input and sets public variables to the values given input.
Author: Corey Fournier
        Sam Gleske
"""
from sys import exit

class SwitchParser:
    """
    F - file
    C - cascade
    N - NSIS Script Output
    Q - Suppress overwrite prompt for NSIS Script Output
    """
    SWITCHES = ["F","C","N","Q"]
    """File name of file passed in"""
    fileName = None
    """NSIS output filename"""
    nsisOutput = None
    """Do not prompt for file overwrites"""
    quietMode = False
    """Delete with cascade is enabled if true/ false otherwise"""
    deleteWithCascade = False
    
    TAB = "\t"
    NEW_LINE = "\n"    
    
    """ Class constructor
        commandLineArguments - Arguments passed in at the command line
    """
    def __init__(self, commandLineArguments):
        arguments = []
        switch = None
        argument = None
        
        if len(commandLineArguments) == 1:
            self.syntaxErr()
        
        """Clean the arguments up"""        
        for argument in commandLineArguments:
            if argument != "" :
                argument = argument.strip()
            if argument != "" :
                arguments.append(argument)
        """Now look at all of the arguments to see if any match"""
        for i in range(len(arguments)):
            argument = arguments[i]
            
            #display help documentation
            if "/?" in argument :
                self.showhelp()
            elif "--help" in argument :
                self.showhelp()
            elif "-help" in argument :
                self.showhelp()

            #see if the current argument is a switch indicator
            try:
                if argument.find("-",0,1)  > -1 :
                    switch = argument.upper()[1:2]
                    if self.SWITCHES.count(switch) > 0 :
                        if self.SWITCHES[0] == switch: #The next argument is a file
                            argument = arguments[i + 1]
                            self.fileName = argument 
                        elif self.SWITCHES[1] == switch: # Delete with cascade is selected
                            self.deleteWithCascade = True
                        elif self.SWITCHES[2] == switch: #The next argument is a file
                            argument = arguments[i + 1]
                            if argument != '' :
                                self.nsisOutput = argument
            except:
                self.syntaxErr()
    def showhelp(self):
        print "Uses a RegShot Plain TXT compare log to stop services, kill executables, and   "
        print "unregister DLL files before doing a file and registry entry removal to ensure  "
        print "the cleanest possible removal of software."
        print ""
        print "REVERTER [-F inFile] [-N outFile] [-C]"
        print ""
        print "  /?" + self.TAB + self.TAB + "Shows this help dialog.  Also -help and --help work."
        print "  -C" + self.TAB + self.TAB + "Delete registry entries with cascade"
        print "  -F" + self.TAB + self.TAB + "Run automatic file/folder/registry removal using inFile as   "
        print self.TAB + self.TAB +          "input unless -N switch is used"
        print "  inFile" + self.TAB +        "Specifies the RegShot file to be read.  Must be Plain TXT!   "
        print "  -N" + self.TAB + self.TAB + "Read -F as input and generate an NSIS script using outFile as"
        print self.TAB + self.TAB +          "output which can be compiled and distributed."
        print "  outFile" + self.TAB +       "Specifies the path of NSIS script file (*.nsi) which will be "
        print self.TAB + self.TAB +          "generated."
        print ""
        print "Created by: Corey Fournier, Michael Venable, and Sam Gleske"
        print "http://sourceforge.net/projects/registrykeyremo"
        exit()
    def syntaxErr(self):
        print "The syntax of the command is incorrect.  Try COMMAND /?."
        exit()