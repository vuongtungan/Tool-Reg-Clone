import subprocess

NOX_CMD = r'G:\Download\LDPlayer\ldconsole.exe '

def createLD(name):
    return subprocess.call(NOX_CMD + ('add --name {0}').format(name),shell=True)

def removeLD(name):
    return subprocess.call(NOX_CMD + ('remove --name {}').format(name),shell=True)

def modify(name, res1, re2, res3, cpu, mem):
    return subprocess.call(NOX_CMD + ('modify --name {0} --resolution {1},{2},{3} --cpu {4} --memory {5}').format(name,res1,re2,res3,cpu,mem),shell=True)

def launchLD(name):
    return subprocess.call(NOX_CMD + ('launch --name {0}').format(name),shell=True)

def startNewLD(i):
    createLD(('NoxPlayer{}').format(i))
    modify(('NoxPlayer{}').format(i),300,400,120,1,2048)
    launchLD(('NoxPlayer{}').format(i))