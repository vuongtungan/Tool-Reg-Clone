import time
import cv2
import random
import threading
import subprocess
import numpy as np

thread_num = 5
threads = []

def openLD(id):

    ld = "G:\Download\LDPlayer\ldconsole.exe " + ("launch --index {0}").format(id)
    subprocess.run(ld,shell=True)

class Device:

    def tap(self,index,x,y):
        return subprocess.run(("adb -s emulator-{0} shell input tap {1} {2}").format(index,x,y))

    def clear_package(self,index, package):
        return subprocess.run(("adb -s emulator-{0} shell pm clear {1}").format(index,package))

    def grant(self, index, package,permission):
        return subprocess.run(("adb -s emulator-{0} shell pm grant {1} {2}").format(index,package,permission))

    def click_ocr(image, device):
        with open("image/screen.png", "wb") as fp:
            screen = device.screencap()

            fp.write(screen)
            fp.close()

        img = cv2.imread(image)

        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        template = cv2.imread("image/screen.png", 0)

        w, h = template.shape[1], template.shape[0]
        res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
        THRESHOLD = 0.8
        loc = np.where(res >= THRESHOLD)

        # Draw boudning box
        for y, x in zip(loc[0], loc[1]):
            return device.tap(x + 4, y + 4)

    def write_vn(self, index, text):
        return subprocess.run(("adb -s emulator-{0} shell input text {1}").format(index,text))

    def uninstall(self, index, package):
        return subprocess.run(("adb -s emulator-{0} uninstall {1}").format(index,package))

    def install(self,index, package):
        return subprocess.run(("adb -s emulator-{0} install {1}").format(index,package))


def regFacebook():
    num = 5552
    device = Device()

    print('Đang uninstall facebook')
    device.uninstall(index=num+2,package='com.facebook.lite')
    time.sleep(2)

    print('Đang install facebooklite')
    device.install(num+2,'apps/fb.apk')
    time.sleep(3)
    num += 2



for i in range(thread_num):
    threads += [threading.Thread(regFacebook())]

for i in threads:
    i.start()

for i in threads:
    i.join()


