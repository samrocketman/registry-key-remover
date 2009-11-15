reverter.exe is the command line version. (for more advanced users)
regshot_reverter.exe is the graphical version (for less advanced users)

Program Authors: Michael Venable
                 Corey Fournier
                 Sam Gleske
Project Website: http://sourceforge.net/projects/registrykeyremo/



**********************
*    IMPORTANT!!!    *
**********************
READ THIS FIRST!
This program is designed to modifiy your registry. Be sure to back up 
your registry before making any changes (SEE FAQ at bottom).  It is 
still a work in progress so there's always no guaruntee that it won't 
damage your registry.  This was designed for 32-bit systems (like 
regshot) so it may or may not work on 64-bit systems.

*Please note: Only the NSIS script Generating is fully working correctly.



**********************
*    reverter.exe    *
**********************
reverter.exe [options]
Options:
    -F filepath : imports your RegShot Compare Log (Plain TXT) where
                  filepath is the path and filename of your text file.
                  This option will automatically revert your registry
                  and filesystem unless -N option is switched.  This
                  option is required in all cases!
             -c : Deletes registry along with it's cascade tree structure.
                  Overrides -F option and is overridden by -N option.
                  -F switch takes no action.
                  -F switch is required.
    -N filepath : Does not make changes to your system.  Instead reverter
                  generates an NSIS script which can easily be compiled.
                  -C switch does nothing in this case.
                  -F switch is required.



**********************
*regshot_reverter.exe*
**********************
Regshot reverter is a nice, simple, GUI front end for reverter.exe. It is
designed to be more user friendly than the command line version.  If you
read the command line options then the GUI will be pretty self explanatory.



**********************
*    Requirements    *
**********************
reverter.exe requires the following files from the package:
library.zip
python26.dll

regshot_reverter.exe:
does not require any of the files from the package

Both files require the following operating system files (not distributed):
taskkill.exe - C:\WINDOWS\system32\taskkill.exe
regsvr32.exe - C:\WINDOWS\system32\regsvr32.exe
net.exe - C:\WINDOWS\system32\net.exe
WSOCK32.dll - C:\WINDOWS\system32\WSOCK32.dll
USER32.dll - C:\WINDOWS\system32\USER32.dll
ADVAPI32.dll - C:\WINDOWS\system32\ADVAPI32.dll
SHELL32.dll - C:\WINDOWS\system32\SHELL32.dll
KERNEL32.dll - C:\WINDOWS\system32\KERNEL32.dll



**********************
*       ~FAQ~        *
**********************
What does this software do?
Reads the filesystem/registry compare log files from the software RegShot 
and then either 1.) Generates an NSIS script that can be compiled by the 
user with NSIS or 2.) Reverts the changes for you without user having to 
compile anything.*


What is NSIS?
Please refer to http://nsis.sourceforge.net/ for more information.


What does the NSIS script do when it is compiled?
The NSIS Script executes in the following order:
1.) Stops all services found
2.) Kills all executable (*.exe) files found
3.) Unregisters all Dynamic Link Libraries (*.dll) found
4.) Deletes all created files
5.) Deletes all created folders
6.) Deletes all created registry values
7.) Deletes all created registry keys
8.) Recommends user to restart and run executable again to ensure 
    software was fully removed.


How to back up registry?
1. Click on Start > Run. (on vista and 7 type run)
2. Type regedit and press enter.
3. Right click on My Computer in the Registry Editor and select Export.  
   (Be sure to remember where you export it to!


How do I import my backed up registry?
1. Double click on your *.reg backup.
2. Alternatively Click on Start > Run. (on vista and 7 type run)
3. Type regedit and press enter.
4. Click on File > Import and import your backed up registry.


I only want registry entries and values to be deleted, not files! How do 
I accomplish this?
At the bottom of the generated script file you'll see the following:
Section "MainSection" SEC01
  Call stopServices
  Call killExecutables
  Call unregisterDLLs
  Call deleteFiles
  Call deleteFolders
  Call deleteValues
  Call deleteKeys
  DetailPrint ""
  DetailPrint "All done, Thanks for using Corey And Mike's Registry 
Reverter."
  DetailPrint "NSIS Script Generator written by Sam Gleske."
  DetailPrint "https://sourceforge.net/projects/registrykeyremo/"
  MessageBox MB_OK "It is recommended to reboot your computer and run 
this auto_reverter again to ensure all entries have been fully removed."
SectionEnd

Remove the lines with stopServices, killExecutables, unregisterDLLs, 
deleteFiles, and deleteFolders.
Section "MainSection" SEC01
  Call deleteValues
  Call deleteKeys
  DetailPrint ""
  DetailPrint "All done, Thanks for using Corey And Mike's Registry 
Reverter."
  DetailPrint "NSIS Script Generator written by Sam Gleske."
  DetailPrint "https://sourceforge.net/projects/registrykeyremo/"
  MessageBox MB_OK "It is recommended to reboot your computer and run 
this auto_reverter again to ensure all entries have been fully removed."
SectionEnd


What do I need to build my own package from source?
Minimum to compile:
TortoiseCVS (To check out the source)
Python 2.6+ (but not above Python 2.6)
py2exe for Python 2.6
7-zip command line version (7za.exe)
NSIS 2.0+

Add Python26 directory path to PATH variable
Add NSIS directory path to PATH variable

Recommended Additional installs for developing:
Eclipse 3.5+
PyDev 1.5+
HM NIS Edit for NSIS