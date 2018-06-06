import time

def TimetoFloat(temps,format="%Y-%m-%d %H:%M:%S"):
    return time.mktime(time.strptime(temps, format))

def FloattoTime(str="",tab=[],format="%Y-%m-%d %H:%M:%S"):
    if tab != []:
        t = []
        for e in tab:
            t.append(time.strftime(format,time.localtime(e)))
        return t
    else:
        return time.strftime(format,time.localtime(str))
