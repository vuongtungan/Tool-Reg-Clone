from ppadb.client import Client as AdbClient
import random
def getDevice(i):
    # Default is "127.0.0.1" and 5037

    client = AdbClient(host="127.0.0.1", port=5037)
    devices = client.devices()
    return devices[i]

device = getDevice(0)

def clear_package(package,device):
    cmd = "pm clear " + package
    return device.shell(cmd)

file1 = open('contacts/ho.txt', 'r',encoding="utf8").readlines()
file2 = open('contacts/phone.txt', 'r').readlines()
file3 = open('contacts/ten.txt', 'r',encoding="utf8").readlines()

def importContac(device):

    clear_package("com.android.providers.contacts",device)
    for i in range(random.randint(10,20)):
        text1 = str(file1[random.randint(0,70)])
        text2 = str(file2[random.randint(0,70)])
        text3 = str(file3[random.randint(0,70)])
        text = text1  + text3
        print(text)
        device.shell('am start -a android.intent.action.INSERT -t vnd.android.cursor.dir/contact -e name "{0}" -e phone {1}'.format(text,text2))
        device.input_keyevent(4)
        device.input_keyevent(4)

importContac(device)