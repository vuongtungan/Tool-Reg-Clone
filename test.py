from ppadb.client import Client as AdbClient


def grant(package, permission,device):
    cmd = "pm grant " + package + permission
    return device.shell(cmd)

def getDevice(i):
    # Default is "127.0.0.1" and 5037

    client = AdbClient(host="127.0.0.1", port=5037)
    devices = client.devices()

    return devices[i]

device = getDevice(0)
grant("com.facebook.katana", " android.permission.CALL_PHONE",device)