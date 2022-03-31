import time
import cv2
import numpy as np
import random
from ppadb.client import Client as AdbClient

def getDevice(i):
    # Default is "127.0.0.1" and 5037

    client = AdbClient(host="127.0.0.1", port=5037)
    devices = client.devices()

    return devices[i]

device = getDevice(0)

def get_cookie(i):

    cmd = ("pull /data/data/com.facebook.katana/files/PropertiesStore_v02 cookie_{0}.txt").format(i)
    device.shell(cmd)

    arrcook = open(('cookie_{0}.txt').format(i)).readlines()
    arrgetcook = arrcook[0].split('"')

    uid = arrgetcook[17]
    xs = arrgetcook[72]
    fr = arrgetcook[98]
    datr = arrgetcook[124]
    token = arrgetcook[11]

    cookie = "c_user=" + uid + ";xs=" + xs + ";fr=" + fr + ";datr=" + datr

    return cookie, token

def write_data(uid, passwd,two_fa, cookie, token, mail):

    with open("veri_account", "a+") as vr:

        vr.write('\n')
        vr.write(uid + "|" + passwd + "|" + two_fa + "|" + cookie + "|" + token + "|" + mail)

cook, token = get_cookie(0)

print(cook,token)