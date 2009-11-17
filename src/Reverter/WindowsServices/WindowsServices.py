'''
@author andy mckay (no email)
@copyright none
@license none
@sourcelink http://code.activestate.com/recipes/59872/
@dependency pywin32 extension for python


Created on Nov 17, 2009
Minor Authors: Sam Gleske
'''
import win32serviceutil

def service_info(service, action = 'status', machine = None):
    if action == 'stop': 
        win32serviceutil.StopService(service, machine)
        print '%s stopped successfully' % service
    elif action == 'start': 
        win32serviceutil.StartService(service, machine)
        print '%s started successfully' % service
    elif action == 'restart': 
        win32serviceutil.RestartService(service, machine)
        print '%s restarted successfully' % service
    elif action == 'status':
        if win32serviceutil.QueryServiceStatus(service, machine)[1] == 4:
            print "%s is running normally" % service 
        else:
            print "%s is *not* running" % service 
