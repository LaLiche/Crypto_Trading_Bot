import time

def TimetoFloat(temps,format="%Y-%m-%d %H:%M:%S"):
    return time.mktime(time.strptime(temps, format))

def FloattoTime(str="",tab=[],format="%Y-%m-%d %H:%M:%S"):
    if tab != []:
        for e in tab:
            time.strftime(format,time.localtime(e))
        return tab
    else:
        return time.strftime(format,time.localtime(str))
