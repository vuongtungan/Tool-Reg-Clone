import subprocess
import sys
NOX_CMD = r'C:\Program Files (x86)\Nox\bin\NoxConsole.exe '

def createLD(name):
    return subprocess.call(NOX_CMD + ('copy -name:{0} -from:NoxPlayer').format(name))

def removeLD(name):
    return subprocess.call(NOX_CMD + ('remove -name:{}').format(name))

def modify(name, res1, re2, res3, cpu, mem):
    return subprocess.call(NOX_CMD + ('modify -name:{0} -resolution:{1},{2},{3} -cpu:{4} -memory:{5}').format(name,res1,re2,res3,cpu,mem))

def launchLD(name):
    return subprocess.call(NOX_CMD + ('launch -name:{0}').format(name))

def close(name):
    return subprocess.call(NOX_CMD + ('quit -name:{0}').format(name))

def startNew(i):
    createLD(('NoxPlayer{}').format(i))
    modify(('NoxPlayer{}').format(i),300,400,120,2,2048)
    launchLD(('NoxPlayer{}').format(i))


startNew(sys.argv[1])
