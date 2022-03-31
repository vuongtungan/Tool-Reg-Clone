import random
from ppadb.client import Client as AdbClient

dir = "data/"
ho = dir + "name/ho.txt"
ten = dir + "name/ten.txt"

file_1 = open(ho, "r",encoding="utf8").readlines()
file_2 = open(ten, "r",encoding="utf8").readlines()

def name():
    return file_2[random.randint(0,212)]

def ToCharArray(text):

    arr = []
    for i in text:
        arr.append(i)
    return arr

def password(email):
    random_pass = ''
    letter = ToCharArray("qwertyuiopasdfghjklzxcvbnm0123456789")

    for i in range(10):

        spec = random.randint(0, 1)
        if spec != 0:
            random_pass += letter[random.randint(0, 35)]
        else:
            random_pass += letter[random.randint(0, 35)].capitalize()

    with open("password.txt", "a+")as fp:
        fp.write('\n')
        fp.write(email + '|' + random_pass)

    return random_pass

def getDevice(i):
    # Default is "127.0.0.1" and 5037

    client = AdbClient(host="127.0.0.1", port=5037)
    devices = client.devices()

    return devices[i]

device = getDevice(0)
device.shell("input text {}".format(name()))

#print(password('tunganhaihai@gmai.com'))
print(name())