import usb.core
import sched
import time
import re
import subprocess

# initialization
devices = []

# create the schedule for events
s = sched.scheduler(time.time, time.sleep)
s.enter(1, 1, reportActiveDevices)
s.run()

# the reportActiveDevices function starts a loop to observe all usb ports and report any 
# active connections
def reportActiveDevices:
    device_re = re.compile(b"Bus\s+(?P<bus>\d+)\s+Device\s+(?P<device>\d+).+ID\s(?P<id>\w+:\w+)\s(?P<tag>.+)$", re.I)
    df = subprocess.check_output("lsusb")
    localDevices = []
    for i in df.split(b'\n'):
        if i:
            info = device_re.match(i)
            if info:
                dinfo = info.groupDict()
                dinfo['device'] = '/dev/bus/usb/%s/%s' % (dinfo.pop('bus'), dinfo.pop('device'))
                localDevices.append(dinfo)
    devices = localDevices
    s.enter(1, 1, reportActiveDevices, ())

