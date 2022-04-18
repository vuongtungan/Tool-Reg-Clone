# -*- coding: utf8 -*-
import time
import cv2
import numpy as np
import random
from ppadb.client import Client as AdbClient
import threading
import requests
from PIL import Image
from pyzbar.pyzbar import decode
import pyotp
import json

thread_num = 1
threads = []


def getDevice(i):
    # Default is "127.0.0.1" and 5037

    client = AdbClient(host="127.0.0.1", port=5037)
    devices = client.devices()

    return devices[i]

dir = "data/"
ho = dir + "name/ho.txt"
ten = dir + "name/ten.txt"



def clear_package(package,device):
    cmd = "pm clear " + package
    return device.shell(cmd)

def enable_wifi(device):
    return device.shell("su -c 'svc wifi enable'")

def disable_wifi(device):
    return device.shell("su -c 'svc wifi disable'")

def grant(package, permission,device):
    cmd = "pm grant " + package + permission
    return device.shell(cmd)

def importContac(device):

    file1 = open('contacts/ho.txt', 'r', encoding="utf8").readlines()
    file2 = open('contacts/phone.txt', 'r').readlines()
    file3 = open('contacts/ten.txt', 'r', encoding="utf8").readlines()
    clear_package("com.android.providers.contacts",device)
    for i in range(random.randint(5,10)):
        text1 = str(file1[random.randint(0,70)])
        text2 = str(file2[random.randint(0,70)])
        text3 = str(file3[random.randint(0,70)])
        text = text1  + text3
        device.shell('am start -a android.intent.action.INSERT -t vnd.android.cursor.dir/contact -e name "{0}" -e phone {1}'.format(text,text2))
        device.input_keyevent(4)
        device.input_keyevent(4)

def open_package(package,device):
    cmd = "monkey -p " + package + " -c android.intent.category.LAUNCHER 1"
    return device.shell(cmd)


def change_lang(device):
    click_ocr('image/more.PNG', device)
    time.sleep(1)

    # for i in range(10):
    #     device.shell('input swipe 138 162 143 13')

    click_ocr('image/tv.PNG', device)

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

def write_vn(text,device):

    for i in range(len(text)):
        time.sleep(0.05)
        device.input_text(text[i])

def ToCharArray(text):
    arr = []
    for i in text:
        arr.append(i)
    return arr

def password():
    random_pass = ''
    letter = ToCharArray("qwertyuiopasdfghjklzxcvbnm0123456789")

    for i in range(10):

        spec = random.randint(0, 1)
        if spec != 0:
            random_pass += letter[random.randint(0, 35)]
        else:
            random_pass += letter[random.randint(0, 35)].capitalize()
    return random_pass

def get_current_proxyTM(api):

    param = {
        "api_key": api
    }
    request = requests.post("https://tmproxy.com/api/proxy/get-current-proxy", json=param).json()
    return request['data']['https']

def get_new_proxyTM(api):

    param = {
        "api_key": api
    }
    request = requests.post("https://tmproxy.com/api/proxy/get-new-proxy", json=param).json()
    return request['data']['https']

def get_number_VOTP(api):

    get = requests.get(("https://api.viotp.com/request/get?token={0}&serviceId=7").format(api)).json()

    number = get['data']['phone_number']
    id = get['data']['request_id']

    return number, id

def get_otp_VOTP(api,id):

    get = requests.get(('https://api.viotp.com/session/get?requestId={0}&token={1}').format(id,api)).json()

    otp = get['data']['Code']

    return otp

def code_2fa(image):
    img = Image.open(image)
    data = str(decode(img)[0][0])

    totp = pyotp.TOTP(data[43:75])
    return totp.now(),data[43:75]

def turn_2fa(device,i):

    device.shell(' am start -a android.intent.action.VIEW '
                 '-d fb://facewebmodal/f?href=https://m.facebook.com/security/2fac/setup/intro')

    time.sleep(3.5)
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
    write_vn(otp,device)
    click_ocr('image/next.PNG', device)
    time.sleep(4)
    click_ocr('image/done.PNG', device)

    return two_fa

def clear_input(n,device):

    device.input_tap(83,190)

    device.shell("input keyevent KEYCODE_MOVE_END")
    for i in range(n):
        time.sleep(0.1)
        device.input_keyevent(67)

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

def change_info(device):

    print("Đang fake info")
    disable_wifi(device)
    open_package("com.unique.mobilefaker",device)
    time.sleep(11)

    for i in range(random.randint(1,3)):
        click_ocr("image/ld/fake_0.PNG",device)

    click_ocr("image/ld/fake_1.PNG", device)
    # device.shell('pm clear com.unique.mobilefaker')

    open_package("com.device.emulator",device)
    time.sleep(3)

    for i in range(random.randint(1,3)):
        click_ocr("image/ld/fake_2.PNG",device)

    click_ocr("image/ld/fake_3.PNG", device)
    time.sleep(1)
    click_ocr("image/ld/fake_4.PNG", device)
    # device.shell('pm clear com.device.emulator')

def getNumber(api):

    param = "&apikey={0}&action=create-request&serviceId=1&count=1".format(api)
    get = requests.get("http://codetextnow.com/api.php",params=param)
    number = json.loads(get.text)['results']['data'][0]
    return number['sdt'], number['requestId']

def getOTP(api,requestid):

    param = "&apikey={0}&action=data-request&requestId={1}".format(api,requestid)
    getCode = requests.get("http://codetextnow.com/api.php",params=param).json()
    otp = getCode['data'][0]['otp']
    return otp

def getMail(api):

    param = "&apikey={0}&action=create-request&serviceId=3&count=1".format(api)
    get = requests.get("http://codetextnow.com/api.php",params=param)
    number = json.loads(get.text)['results']['data'][0]
    return number['email'], number['requestId']

def getOTPMail(api,requestid):

    param = "&apikey={0}&action=data-request-tempmail&requestId={1}".format(api,requestid)
    getCode = requests.get("http://codetextnow.com/api.php",params=param).json()
    otp = getCode['data'][0]['otp']
    return otp

def name():
    name, mid = '',''
    file_1 = open(ho, "r", encoding="utf8").readlines()
    file_1 = file_1[random.randint(0,1375)]
    for i in range(len(file_1)):
        if file_1[i] == ' ':
            name = file_1[:i]
            mid = file_1[i+1:]
    return name,mid

def LDregFacebook(i):


    file_1 = open(ho, "r", encoding="utf8").readlines()
    file_2 = open(ten, "r", encoding="utf8").readlines()

    device = getDevice(i)

    #change_info(device)

    # print("Đang nhập proxy")
    #
    # proxy = get_new_proxyTM('c86fbeaca7eb5a4b2fb07d3697410bab')
    #
    # if proxy == '':
    #     proxy = get_current_proxyTM('c86fbeaca7eb5a4b2fb07d3697410bab')
    #
    # device.shell(("settings put global http_proxy {}").format(proxy))
    print('Đang uninstall facebook')
    device.uninstall('com.facebook.katana')
    time.sleep(1)

    importContac(device)

    print('Đang install facebook')
    device.install('apps/facebook.apk')
    # time.sleep(1)

    #enable_wifi(device)


    print("Đang xóa dữ liệu Facebook")
    clear_package("com.facebook.katana",device)


    print("Đang cho phép các quyền")
    grant("com.facebook.katana", " android.permission.READ_CONTACTS",device)
    grant("com.facebook.katana", " android.permission.CALL_PHONE",device)
    grant("com.facebook.katana", " android.permission.CAMERA",device)
    grant("com.facebook.katana", " android.permission.ACCESS_FINE_LOCATION",device)
    grant("com.facebook.katana", " android.permission.READ_EXTERNAL_STORAGE",device)

    time.sleep(0.5)
    print("Đang mở Facebook")
    device.shell("monkey -p com.facebook.katana -c android.intent.category.LAUNCHER 1")

    time.sleep(20)

    change_lang(device)
    time.sleep(1)

    print("Nhấn Tạo tài khoản...")
    click_ocr("image/create.PNG",device)

    time.sleep(12)
    print("Nhấn Next...")
    click_ocr("image/next.PNG",device)
    time.sleep(2)

    # Cần đọc vào file
    sir,mid = name()

    print("Đang nhập họ và tên")
    time.sleep(random.randint(1,2))
    write_vn(sir,device)

    device.input_tap(177,188)
    write_vn(mid,device)
    device.input_keyevent(62)
    last_n = file_2[random.randint(0,212)]
    write_vn(last_n,device)
    time.sleep(random.randint(1,2))

    print("Nhấn next")
    click_ocr("image/next.PNG",device)
    time.sleep(random.randint(1,2))

    print("Điền ngày tháng năm...")
    time.sleep(random.randint(1,2))
    click_ocr("image/birthday.PNG", device)
    time.sleep(0.5)
    device.input_tap(100, 204)
    write_vn(str(random.randint(1,29)), device)
    device.input_keyevent(61)
    time.sleep(random.randint(1,2))
    device.input_keyevent(61)
    write_vn(str(random.randint(1970,2000)), device)
    time.sleep(random.randint(1,2))
    click_ocr('image/ok_bthd.PNG', device)
    time.sleep(random.randint(1, 2))
    click_ocr("image/next.PNG",device)
    time.sleep(random.randint(1,2))

    print("Điền giới tính")
    click_ocr('image/gender.PNG',device)
    time.sleep(random.randint(0,1))
    click_ocr("image/next.PNG",device)
    time.sleep(random.randint(1,2))

    print("Đang điền số điện thoại")
    # clear_input(13,device)
    # time.sleep(random.randint(1,2))
    click_ocr("image/reg_by_mail.PNG", device)
    time.sleep(random.randint(1,2))

    # number, id = getNumber('651fd893615c82eb86ed8a45bfd15965')
    # write_vn('+1'+ number,device)
    number, id = getMail('651fd893615c82eb86ed8a45bfd15965')
    write_vn(number,device)
    time.sleep(random.randint(1,2))
    click_ocr('image/next.PNG',device)

    time.sleep(random.randint(1,2))
    print("Nhập password")
    passwd = last_n + str(random.randint(0,9))
    write_vn(passwd, device)
    time.sleep(random.randint(1,2))
    click_ocr("image/next.PNG",device)
    time.sleep(random.randint(1,2))

    print("Đang tạo tài khoản")
    click_ocr("image/regist.PNG",device)
    time.sleep(40)

    click_ocr('image/other.PNG',device)
    time.sleep(random.randint(1,2))
    click_ocr('image/ok.PNG',device)
    time.sleep(random.randint(1,2))

    while True:
        time.sleep(random.randint(1,2))
        otp = getOTPMail('651fd893615c82eb86ed8a45bfd15965',id)
        if otp != None:
            break

    write_vn(otp,device)
    time.sleep(random.randint(1,2))
    click_ocr('image/confirm.PNG',device)
    time.sleep(10)

    click_ocr('image/skip.PNG',device)
    time.sleep(10)
    click_ocr("image/skip.PNG",device)
    time.sleep(random.randint(1,2))
    click_ocr("image/skip.PNG", device)
    time.sleep(random.randint(1, 2))
    click_ocr('image/other.PNG',device)

    print("Đang hoàn tất reg")
    time.sleep(3)
    print('Đang lấy 2fa')
    two_fa = turn_2fa(device, i)

    print("Đã reg xong")

    with open("password_2fa.txt", "a+")as fp:
        fp.write('\n')
        fp.write(number + '|' + passwd + '|' + two_fa)

    time.sleep(1)
    print("Đang log out")

    logout(device)
    time.sleep(3)

    print("Đang reg tiếp theo...")

for i in range(thread_num):
    t0 = threading.Thread(target=LDregFacebook, args=(0,))
    #t1 = threading.Thread(target=regFacebook, args=(1,))
    #t2 = threading.Thread(target=regFacebook, args=(2,))
    #t3 = threading.Thread(target=regFacebook, args=(3,))
    #t4 = threading.Thread(target=regFacebook, args=(4,))
    t0.start()
    #t1.start()
    #t2.start()
    #t3.start()
    #t4.start()
    t0.join()
    #t1.join()
    #t2.join()
    #t3.join()
    #t4.join()

