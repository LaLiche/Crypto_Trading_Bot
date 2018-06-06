import time

def TimetoFloat(temps,format="%Y-%m-%d %H:%M:%S"):
    return time.mktime(time.strptime(temps, format))

def FloattoTime(str,format="%Y-%m-%d %H:%M:%S"):
    return time.strftime(format,time.localtime(str))
