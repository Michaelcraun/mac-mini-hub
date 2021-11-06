import os
import time
from datetime import date

# dev imports
import random

maximumCriticalEventCount = 0
maximumTemp = 70.0
logfileName = "temp_log.txt"

criticalEventCount = 0
isOverheating = False

def initMonitorWithMaxTemp(max = 70.0, count = 3, logfile = "temp_log.txt"):
    global logfileName
    global maximumCriticalEventCount
    global maximumTemp
    logfileName = logfile
    maximumCriticalEventCount = count
    maximumTemp = max
    newLogSet()
    
def newLogSet():
    today = date.today()
    log("\nStarting new monitor on {}".format(today))

def measureTemp():
    # generate random numbers for development (vcgencmd is a Pi-specific command)
    # temp = os.popen("vcgencmd measure_temp").readline()
    randomTemp = random.uniform(80.0,120.0)
    temp = 'temp={}'.format(randomTemp)
    string = (temp.replace("temp=",""))
    return float(string)
    
def log(message):
    global logfileName
    file = open(logfileName, "a")
    file.write("{}\n".format(message))
    file.close()
    
def startTempMonitor():
    while True:
        global criticalEventCount
        global isOverheating
        global maximumCriticalEventCount
        global maximumTemp
        
        currentTemp = measureTemp()
        if isOverheating:
            if currentTemp < maximumTemp:
                log("Temperature has dropped to a nominal range [{}]".format(currentTemp))
                isOverheating = False
                criticalEventCount = 0
            else:
                log("WARN: Temperature is {}".format(currentTemp))
                criticalEventCount += 1
                if criticalEventCount > maximumCriticalEventCount:
                    log("ERR: Temperature was too hot for too long")
                    print("[PiTemp] A critical temperature has been reached! Logs can be found in 'temp_log.txt' in your project's root directory.")
                    return True
        else:
            if currentTemp > maximumTemp:
                log("WARN: Temp is too high [{}]".format(currentTemp))
                isOverheating = True
        time.sleep(1)
