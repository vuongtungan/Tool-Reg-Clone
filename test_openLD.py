import subprocess
import random
LD_CMD = r'G:\Download\LDPlayer\ldconsole.exe '
file1 = open('contacts/phone.txt', 'r').readlines()

def createLD(name):
    return subprocess.call(LD_CMD + ('add --name {0}').format(name),shell=True)

def removeLD(name):
    return subprocess.call(LD_CMD + ('remove --name {}').format(name),shell=True)

def modify(name, res1, re2, res3, cpu, mem):
    pnum = file1[random.randint(0,7749)]
    manu = "samsung"
    model = ["SM-G9730", "SM-G9750", "SM-N9760", "SM-G988N", "SM-G965N", "SM-G9880", "SM-G9810"]
    subprocess.call(LD_CMD + ('modify --name {0} --resolution {1},{2},{3} --cpu {4} --memory {5}').format(name,res1,re2,res3,cpu,mem,))
    subprocess.call(LD_CMD + ("modify --name {0} --pnumber {1} --manufacturer {2} --model {3}").format(name,pnum,manu,model[random.randint(0,len(model)-1)]))


def launchLD(name):
    return subprocess.call(LD_CMD + ('launch --name {0}').format(name),shell=True)

def startNewLD(i):
    createLD(('LDPlayer-{}').format(i))
    modify(('LDPlayer-{}').format(i),300,400,120,1,2048)
    launchLD(('LDPlayer-{}').format(i))

startNewLD(2)