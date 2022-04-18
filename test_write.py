from ppadb.client import Client as AdbClient
import time
def getDevice(i):
    # Default is "127.0.0.1" and 5037

    client = AdbClient(host="127.0.0.1", port=5037)
    devices = client.devices()

    return devices[i]

def write_vn(text,device):
    #
    # device.shell("ime set com.android.adbkeyboard/.AdbIME")
    # device.shell("am broadcast -a ADB_INPUT_B64 --es msg {}".format(text))
    for i in range(len(text)):
        time.sleep(0.05)
        device.input_text(text[i])

device = getDevice(0)
write_vn('Tùng An',device)