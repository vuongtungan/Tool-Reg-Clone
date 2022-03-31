import cv2
import numpy as np
from ppadb.client import Client as AdbClient
from time  import sleep

def location(image,device,id):
    while True:

        sleep(0.4)
        with open(("image/screen_{0}.png").format(id), "wb") as fp:
            screen = device.screencap()

            fp.write(screen)
            fp.close()

        img = cv2.imread(image)

        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        template = cv2.imread(("image/screen_{0}.png").format(id), 0)
        res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
        THRESHOLD = 0.9
        loc = np.where(res >= THRESHOLD)

        # Draw boudning box
        for y, x in zip(loc[0], loc[1]):
            a = device.input_tap(x + 6, y + 6)
            if a != None:
                break
        break


def getDevice():
    # Default is "127.0.0.1" and 5037
    client = AdbClient(host="127.0.0.1", port=5037)
    devices = client.devices()
    if (len(devices) < 0):
        print("0 device")
        return 0

    return devices[0]

device = getDevice()

print(location("image/next.PNG",device,0))
