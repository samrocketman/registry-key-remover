'''
Created on Nov 20, 2009

@author: Sam Gleske
'''
import win32process, win32gui
from win32com.client import GetObject


def killImage(imageName) :
    WMI = GetObject('winmgmts:')
    processes = WMI.InstancesOf('Win32_Process')
    process_list = [(p.Properties_("ProcessID").Value, p.Properties_("Name").Value) for p in processes]
    for a in process_list :
        for b in a :
            print b
    pid = win32process.GetProcessId(imageName)
    print win32gui.EnumWindows()
    if not killProcess(pid) :
        print "force kill!"
    else :
        print "killed!"
def killProcess(pid):
    print str(pid)
#def fkillProcess(imageName):
killProcess("calc.exe")