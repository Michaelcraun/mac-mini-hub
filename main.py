# import usb.core
import sched
import time
import re
import subprocess
import os

from util.date import Date
from util.emailer import PiMailer
from util.temp import PiTemp

class Main:
    # constants
    logfile = 'logs.txt'
    
    # monitoring
    criticalTemp = False
    
    # setup utilities
    mailer = PiMailer('smtp.gmail.com', 587, 'ras.pi.craun@gmail.com', 'dymdu9-vowjIt-kejvah')
    tempMonitor = PiTemp(80.0, 3, logfile)
    
    # Since this is either a brand-new run and logs have already been reviewed or the start of a new month, 
    # we want to blow away any old log file(s) and start a fresh one
    def cleanLogs(self):
        if os.path.exists(self.logfile):
            os.remove(self.logfile)
            
        file = open(self.logfile, 'a')
        file.write('Starting new logs [{}]\n'.format(Date().timestamp()))
        file.close()
        
    def reportCriticalEvent(self):
        subject = 'Oh, no! Your RasPi has encountered a critical event...'
        body = ''
        
        if self.criticalTemp:
            body += 'Your RasPi has reached and maintained a critical temperature for too long!\n'
            body += 'Log files from your RasPi have been attached below for your convenience.\n'
            body += 'Please take some time to diagnose and fix the issue and then restart your RasPi. :)\n\n'
            
        self.mailer.sendMail('michael.craun@gmail.com', subject, body, ['logs.txt'])
        
    # Start any safety monitors we want running. At the time of writing, this is just the temp monitor.
    def startMonitors(self):
        self.criticalTemp = self.tempMonitor.start()
        
        while True:
            if self.criticalTemp:
                self.reportCriticalEvent()
                exit()
    
    def __init__(self):
        # Fresh run, so blow away the old logs
        self.cleanLogs()
        
main = Main()
main.startMonitors()

# # initialization
# devices = []
# 
# # create the schedule for events
# s = sched.scheduler(time.time, time.sleep)
# s.enter(1, 1, reportActiveDevices)
# s.enter(1, 1, printTemp)
# s.run()
# 
# # the reportActiveDevices function starts a loop to observe all usb ports and report any 
# # active connections
# def reportActiveDevices():
#     device_re = re.compile(b"Bus\s+(?P<bus>\d+)\s+Device\s+(?P<device>\d+).+ID\s(?P<id>\w+:\w+)\s(?P<tag>.+)$", re.I)
#     df = subprocess.check_output("lsusb")
#     localDevices = []
#     for i in df.split(b'\n'):
#         if i:
#             info = device_re.match(i)
#             if info:
#                 dinfo = info.groupDict()
#                 dinfo['device'] = '/dev/bus/usb/%s/%s' % (dinfo.pop('bus'), dinfo.pop('device'))
#                 localDevices.append(dinfo)
#     devices = localDevices
#     s.enter(1, 1, reportActiveDevices, ())