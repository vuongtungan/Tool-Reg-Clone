from ppadb.client import Client as AdbClient
from pyzbar.pyzbar import decode
import pyotp
import time
import cv2
import numpy as np
from PIL import Image

img = 'image/test.PNG'

def code_2fa(image):
    img = Image.open(image)
    data = str(decode(img)[0][0])

    totp = pyotp.TOTP(data[43:75])
    return totp.now(),data[43:75]


#print(code_2fa(img))

def getDevice(i):
    # Default is "127.0.0.1" and 5037

    client = AdbClient(host="127.0.0.1", port=5037)
    devices = client.devices()

    return devices[i]


device = getDevice(0)

def click_ocr(image,device):
    with open("image/screen.png", "wb") as fp:
        screen = device.screencap()

        fp.write(screen)
        fp.close()

    img = cv2.imread(image)

    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    template = cv2.imread("image/screen.png", 0)

    res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
    THRESHOLD = 0.9
    loc = np.where(res >= THRESHOLD)

    # Draw boudning box
    for y, x in zip(loc[0], loc[1]):
        if x == None or y == None:
            return False
        return device.input_tap(x+6,y+6)

def turn_2fa(device,i):

    device.shell(' am start -a android.intent.action.VIEW '
                 '-d fb://facewebmodal/f?href=https://m.facebook.com/security/2fac/setup/intro')

    time.sleep(2)
    click_ocr("image/use_app.PNG",device)
    time.sleep(2)
    for i in range(3):
        device.shell('input swipe 138 162 143 13')
    time.sleep(2)
    with open(("image/2fa_{}.png").format(i), "wb") as fp:
        screen = device.screencap()

        fp.write(screen)
        fp.close()

    otp,two_fa = code_2fa("image/2fa_{}.png".format(i))

    click_ocr('image/next.PNG',device)
    time.sleep(1)
    click_ocr('image/code.PNG',device)
    time.sleep(1)
    device.input_text(otp)
    click_ocr('image/next.PNG', device)
    time.sleep(4)
    click_ocr('image/done.PNG', device)

    return two_fa

#turn_2fa(device,0)
#device.shell(' am start -a android.intent.action.VIEW '
#                 '-d fb://facewebmodal/f?href=https://m.facebook.com/security/2fac/setup/intro')

def logout(device):

    time.sleep(2)
    click_ocr("image/back.PNG", device)
    time.sleep(1)

    click_ocr("image/back.PNG", device)
    time.sleep(1)

    click_ocr("image/back.PNG", device)
    time.sleep(1)

    click_ocr("image/back.PNG", device)
    time.sleep(1)

    click_ocr("image/menu.PNG",device)
    time.sleep(1)
    for i in range(2):
        device.shell('input swipe 138 162 143 13')

    click_ocr("image/logout.PNG",device)

logout(device)