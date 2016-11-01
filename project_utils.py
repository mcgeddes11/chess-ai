import numpy, os, pandas, uuid, re
from subprocess import check_output

def createOutputDirectoryFromFilename(fileName):
    dirName = os.path.dirname(fileName)
    if not os.path.exists(dirName):
        os.makedirs(dirName)

def ping(host):
    import os, platform
    if platform.system().lower() == "windows":
        ping_str = "-n 1"
    else:
        ping_str = "-c 1"
    return os.system("ping " + ping_str + " " + host) == 0

def ismember(a, b):
    bind = {}
    for elt in b:
        if elt not in bind:
            bind[elt] = True
    return numpy.array([bind.get(itm, False) for itm in a])
