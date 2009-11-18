"""
    Main driver for application
    Author: Corey Fournier
            Sam Gleske
"""
from EntryList.RegShotListReader import RegShotListReader
from WindowsRegistry.WindowsRegistry import WindowsRegistry, RegistryKey, WindowsRegistryException
from SwitchParser import *
import sys, re

TAB = "\t"
NEW_LINE = "\n"
FILE_NAME_ARGUMENT_POSITION = 1

sp = SwitchParser(sys.argv)
""" Exit if there is not file name. The class handles the error messages."""
if sp.fileName == None : sp.syntaxErr()

registryInterface = WindowsRegistry()
try:
    registryList = RegShotListReader(sp.fileName)
except IOError:
    print 'inFile: "' + sp.fileName + '" does not exist!'
    print sp.syntaxErr()
except:
    print sp.syntaxErr()

""" If user gave -N FILE_OUTPUT_NAME then generate an NSIS script instead of removing entries """
if sp.nsisOutput != None:
    executables = []
    services = []
    service_keys = []
    registeredDLLs = []
    try:
        f = open(sp.nsisOutput, 'w')
    except:
        sp.syntaxErr()
    """ Generate the beginning of the NSIS File """
    f.write('; Script generated by Reverter for RegShot' + NEW_LINE)
    f.write('; https://sourceforge.net/projects/registrykeyremo/' + NEW_LINE)
    f.write('; NSIS Script Generating implementation created by Sam Gleske (sag47)' + NEW_LINE)
    f.write('; http://www.gleske.net/' + NEW_LINE)
    f.write(NEW_LINE)
    f.write('XPStyle on' + NEW_LINE)
    f.write('CRCCheck on' + NEW_LINE)
    f.write('RequestExecutionLevel admin' + NEW_LINE)
    f.write(NEW_LINE)
    f.write('; Best Compression' + NEW_LINE)
    f.write('SetCompress Auto' + NEW_LINE)
    f.write('SetCompressor /SOLID lzma' + NEW_LINE)
    f.write('SetCompressorDictSize 32' + NEW_LINE)
    f.write('SetDatablockOptimize On' + NEW_LINE)
    f.write(NEW_LINE)
    f.write('Name "Reverter NSIS Script"' + NEW_LINE)
    f.write('OutFile "auto_revert.exe"' + NEW_LINE)
    f.write('InstallDir "$TEMP"' + NEW_LINE)
    f.write('Icon "${NSISDIR}\Contrib\Graphics\Icons\modern-install.ico"' + NEW_LINE)
    f.write('BrandingText "RegShot Reverter"' + NEW_LINE)
    f.write('ShowInstDetails show' + NEW_LINE)
    f.write(';SilentInstall silent' + NEW_LINE)
    f.write(NEW_LINE)

    """ Write and initialization function that avoids errors by allowing only once instance of the program and checking for dependencies """
    f.write('Function .onInit' + NEW_LINE)
    f.write('; Check to ensure all required dependencies are met by the program' + NEW_LINE)
    f.write('  IfFileExists "$SYSDIR\\taskkill.exe" +3' + NEW_LINE)
    f.write('    MessageBox MB_OK|MB_TOPMOST|MB_SETFOREGROUND|MB_ICONSTOP "Required Dependency Warning! $SYSDIR\\taskkill.exe does not exist."' + NEW_LINE)
    f.write('    Quit' + NEW_LINE)
    f.write('  IfFileExists "$SYSDIR\\regsvr32.exe" +3' + NEW_LINE)
    f.write('    MessageBox MB_OK|MB_TOPMOST|MB_SETFOREGROUND|MB_ICONSTOP "Required Dependency Warning! $SYSDIR\\regsvr32.exe does not exist."' + NEW_LINE)
    f.write('    Quit' + NEW_LINE)
    f.write('  IfFileExists "$SYSDIR\\net.exe" +3' + NEW_LINE)
    f.write('    MessageBox MB_OK|MB_TOPMOST|MB_SETFOREGROUND|MB_ICONSTOP "Required Dependency Warning! $SYSDIR\\net.exe does not exist."' + NEW_LINE)
    f.write('    Quit' + NEW_LINE)
    f.write('; Check if already running' + NEW_LINE)
    f.write('; If so don\'t open another but bring to front' + NEW_LINE)
    f.write('  System::Call "kernel32::CreateMutexA(i 0, i 0, t \'$(^Name)\') i .r0 ?e"' + NEW_LINE)
    f.write('  Pop $0' + NEW_LINE)
    f.write('  StrCmp $0 0 launch' + NEW_LINE)
    f.write('   StrLen $0 "$(^Name)"' + NEW_LINE)
    f.write('   IntOp $0 $0 + 1' + NEW_LINE)
    f.write('  loop:' + NEW_LINE)
    f.write('    FindWindow $1 \'#32770\' \'\' 0 $1' + NEW_LINE)
    f.write('    IntCmp $1 0 +4' + NEW_LINE)
    f.write('    System::Call "user32::GetWindowText(i r1, t .r2, i r0) i."' + NEW_LINE)
    f.write('    StrCmp $2 "$(^Name)" 0 loop' + NEW_LINE)
    f.write('    MessageBox MB_OK "Another instance of this program is currently running!"' + NEW_LINE)
    f.write('    System::Call "user32::ShowWindow(i r1,i 9) i."         ; If minimized then maximize' + NEW_LINE)
    f.write('    System::Call "user32::SetForegroundWindow(i r1) i."    ; Brint to front' + NEW_LINE)
    f.write('    Abort' + NEW_LINE)
    f.write('  launch:' + NEW_LINE)
    f.write('FunctionEnd' + NEW_LINE)
    f.write(NEW_LINE)
    
    """ Generate commands to delete all registry key names/values """
    f.write('Function deleteValues' + NEW_LINE)
    f.write('; Delete all registry key names/values' + NEW_LINE)
    f.write('  DetailPrint "Removing Registry Values..."' + NEW_LINE)
    for line in registryList.getValues():
        if line.startswith("HKLM") :
            root_key = line.split('\\',1)[0]
            str1 = line.split(': ')[0]
            p = re.compile("[A-Z]:+")
            str2 = p.split(str1.split('\\',1)[1])[0];
            str3 = str2.split(":")[0]
            sub_key = str3.rsplit('\\',1)[0]
            key_name = str1.split(sub_key + '\\')[1]
            f.write('  DeleteRegValue {0} "{1}" "{2}"'.format( root_key, sub_key, key_name ) + NEW_LINE)
        elif line.startswith("HKU") :
            root_key = line.split('\\',1)[0]
            str1 = line.split(': ')[0]
            p = re.compile("[A-Z]:+")
            str2 = p.split(str1.split('\\',1)[1])[0];
            str3 = str2.split(":")[0]
            sub_key = str3.rsplit('\\',1)[0]
            key_name = str1.split(sub_key + '\\')[1]
            f.write('  DeleteRegValue {0} "{1}" "{2}"'.format( root_key, sub_key, key_name ) + NEW_LINE)
            
    f.write('FunctionEnd' + NEW_LINE)
    f.write(NEW_LINE)
    
    """ Generate commands to delete all registry sub keys that were created """
    f.write('Function deleteKeys' + NEW_LINE)
    f.write('; Delete all registry Keys' + NEW_LINE)
    f.write('  DetailPrint "Removing Registry Keys..."' + NEW_LINE)
    print "Services found at: "
    for line in registryList.getKeys():
        if "SYSTEM\\CurrentControlSet\\Services" in line :
            service_match = "false"
            for temp in service_keys :
                if temp == line.split('\\')[4] :
                    service_match = "true"
            if service_match != "true" :
                if line.split('\\')[4] != "Eventlog" :
                    print "  " + line
                    service_keys.append(line.split('\\')[4])
                    services.append(line)
        f.write('  DeleteRegKey {0} "{1}"'.format( line.split('\\',1)[0], line.split('\\',1)[1] ))
        f.write( NEW_LINE )
    if len(services) == 0 :
        print "  None"
    f.write('FunctionEnd' + NEW_LINE)
    f.write(NEW_LINE)
    
    """ Generate commands to delete all files """
    f.write('Function deleteFiles' + NEW_LINE)
    f.write('; Delete All Files' + NEW_LINE)
    f.write('  DetailPrint "Deleting all files..."' + NEW_LINE)
    print "Executables and Dynamic Link Libraries found at: "
    for line in registryList.getFiles():
        if line.endswith("exe") :
            i = 0
            for temp in line.split('\\') :
                i = i + 1
            print "  " + line
            executables.append(line.split('\\')[i-1])
        elif line.endswith("dll") :
            print "  " + line
            registeredDLLs.append(line)
        f.write('  Delete "' + line + '"' + NEW_LINE)
    if len(executables) == 0 :
        print "  None"
    f.write('FunctionEnd' + NEW_LINE)
    f.write(NEW_LINE)
    
    """ Generate commands to delete all folders """
    f.write('Function deleteFolders' + NEW_LINE)
    f.write('; Delete all folders' + NEW_LINE)
    f.write('  DetailPrint "Deleting All Folders..."' + NEW_LINE)
    for line in registryList.getFolders():
        f.write('  RMDir /r "' + line + '"' + NEW_LINE)
    f.write('FunctionEnd' + NEW_LINE)
    f.write(NEW_LINE)
    
    """ Generate commands to stop all services """
    f.write('Function stopServices' + NEW_LINE)
    f.write('; Stop all services (if service doesn\'t exist then don\'t execute the command)' + NEW_LINE)
    for line in services :
        f.write('  ReadRegStr $0 {0} "{1}" "DisplayName"'.format( line.split('\\',1)[0], line.split('\\',1)[1] ))
        f.write( NEW_LINE )
        f.write('    StrCmp $0 "" +3' + NEW_LINE)
        f.write('    DetailPrint "Stop Service: $0"' + NEW_LINE)
        f.write('    nsExec::ExecToLog "net stop $\\"$0$\\""' + NEW_LINE)
    f.write('FunctionEnd' + NEW_LINE)
    f.write(NEW_LINE)
    
    """ Generate commands to kill all executables (*.exe) """
    f.write('Function killExecutables' + NEW_LINE)
    f.write('; Kill all executables' + NEW_LINE)
    for line in executables :
        f.write('  DetailPrint "Kill EXE: ' + line + '"' + NEW_LINE)
        f.write('  nsExec::ExecToLog "taskkill /IM $\\"' + line + '$\\""' + NEW_LINE)
    f.write('FunctionEnd' + NEW_LINE)
    f.write(NEW_LINE)
    
    """ Generate commands to unregister all Dynamic Link Libraries (*.dll) """
    f.write('Function unregisterDLLs' + NEW_LINE)
    f.write('; unregister all Dynamic Link Libraries' + NEW_LINE)
    for line in registeredDLLs :
        f.write('  nsExec::ExecToLog "regsvr32 /u /s $\\"' + line + '$\\""' + NEW_LINE)
    f.write('FunctionEnd' + NEW_LINE)
    f.write(NEW_LINE)

    f.write('Section "MainSection" SEC01' + NEW_LINE)
    f.write('  MessageBox MB_YESNO|MB_ICONQUESTION|MB_SETFOREGROUND|MB_DEFBUTTON2 "Are you sure you wish to revert your system?  These changes can\'t be undone!" idYes +2' + NEW_LINE)
    f.write('  Quit' + NEW_LINE)
    f.write('  Call stopServices' + NEW_LINE)
    f.write('  Call killExecutables' + NEW_LINE)
    f.write('  Call unregisterDLLs' + NEW_LINE)
    f.write('  Call deleteFiles' + NEW_LINE)
    f.write('  Call deleteFolders' + NEW_LINE)
    f.write('  Call deleteValues' + NEW_LINE)
    f.write('  Call deleteKeys' + NEW_LINE)
    f.write('  DetailPrint ""' + NEW_LINE)
    f.write('  DetailPrint "All done, Thanks for using Corey And Mike\'s Registry Reverter."' + NEW_LINE)
    f.write('  DetailPrint "NSIS Script Generator written by Sam Gleske."' + NEW_LINE)
    f.write('  DetailPrint "https://sourceforge.net/projects/registrykeyremo/"' + NEW_LINE)
    f.write('  MessageBox MB_OK "It is recommended to reboot your computer and run this auto_reverter again to ensure all entries have been fully removed."' + NEW_LINE)
    f.write('SectionEnd' + NEW_LINE)
    f.close()
elif sp.deleteWithCascade :
    print "Deleting all keys with cascade\n"
    for line in registryList.getKeys():
        print TAB + "Removing: " + line
        keyInstance = RegistryKey(line.strip())
        try:
            registryInterface.removeKeyCascade(keyInstance)      
        except WindowsRegistryException, (errno, strerror):
            """ Ignore the error because there is no telling were the cascade will be"""
            if errno == 2 :
                pass   

else : 
    print "Processing all keys\n"
    for line in registryList.getKeys():
        print TAB + "Removing: " + line
        keyInstance = RegistryKey(line.strip())
        try:
            registryInterface.removeKey(keyInstance)
        except WindowsRegistryException, e:
            print e
    
    print NEW_LINE
    print "Processing all values\n"
    
    for line in registryList.getValues():
        if line.startswith("HKLM") :
            print TAB + "Removing: " + line
            keyInstance = RegistryKey(line.strip())
            try:
                registryInterface.removeValue(keyInstance)
            except WindowsRegistryException, e:
                print e
        elif line.startswith("HKU") :
            print TAB + "Removing: " + line
            keyInstance = RegistryKey(line.strip())
            try:
                registryInterface.removeValue(keyInstance)
            except WindowsRegistryException, e:
                print e
   
print NEW_LINE    
print "All done, Thanks for using Corey And Mike's Registry Reverter."
print "NSIS Script Generator written by Sam Gleske."
print NEW_LINE


