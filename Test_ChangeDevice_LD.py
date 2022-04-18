from ppadb.client import Client as AdbClient
import random
import time
import cv2
import numpy as np

def getDevice(i):
    # Default is "127.0.0.1" and 5037

    client = AdbClient(host="127.0.0.1", port=5037)
    devices = client.devices()

    return devices[i]

device = getDevice(0)

def open_package(package,device):
    cmd = "monkey -p " + package + " -c android.intent.category.LAUNCHER 1"
    return device.shell(cmd)

def click_ocr(image,device):
    with open("image/screen.png", "wb") as fp:
        screen = device.screencap()

        fp.write(screen)
        fp.close()

    img = cv2.imread(image)

    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    template = cv2.imread("image/screen.png", 0)

    w, h = template.shape[1], template.shape[0]
    res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
    THRESHOLD = 0.9
    loc = np.where(res >= THRESHOLD)

    # Draw boudning box
    for y, x in zip(loc[0], loc[1]):

        return device.input_tap(x+6,y+6)

def change_info():

    print("Đang fake info")
    open_package("com.unique.mobilefaker",device)
    time.sleep(13)

    for i in range(random.randint(1,3)):
        click_ocr("image/ld/fake_0.PNG",device)

    click_ocr("image/ld/fake_1.PNG", device)

    time.sleep(1)
    open_package("com.device.emulator",device)
    time.sleep(3)

    for i in range(random.randint(1,3)):
        click_ocr("image/ld/fake_2.PNG",device)

    click_ocr("image/ld/fake_3.PNG", device)
    time.sleep(1)
    click_ocr("image/ld/fake_4.PNG", device)


change_info()
