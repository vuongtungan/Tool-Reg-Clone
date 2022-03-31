from ppadb.client import Client as AdbClient

def getDevice(i):
    # Default is "127.0.0.1" and 5037

    client = AdbClient(host="127.0.0.1", port=5037)
    devices = client.devices()

    return devices[i]

device = getDevice(0)

def clear_input(n,device):

    device.input_tap(138,162)
    for i in range(n):
        device.input_keyevent(67)

clear_input(10,device)