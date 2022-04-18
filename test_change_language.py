from ppadb.client import Client as AdbClient
import cv2
import numpy as np
import time

def getDevice(i):
    # Default is "127.0.0.1" and 5037

    client = AdbClient(host="127.0.0.1", port=5037)
    devices = client.devices()

    return devices[i]

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

def change_lang(device):

    click_ocr('image/more.PNG',device)
    time.sleep(1)

    for i in range(10):
        device.shell('input swipe 138 162 143 13')

    click_ocr('image/tv.PNG',device)

device = getDevice(0)
change_lang(device)