# -*- coding: utf8 -*-
import time
import cv2
import numpy as np
import random
from ppadb.client import Client as AdbClient
import threading
import subprocess
import requests
import json
from PIL import Image
from pyzbar.pyzbar import decode
import pyotp


thread_num = 10
threads = []

NOX_CMD = r'C:\Program Files (x86)\Nox\bin\NoxConsole.exe '

def createNox(name):
    return subprocess.call(NOX_CMD + ('copy -name:{0} -from:NoxPlayer').format(name))

def removeNox(name):
    return subprocess.call(NOX_CMD + ('remove -index:{}').format(name))

def modifyNox(name, res1, re2, res3, cpu, mem):
    return subprocess.call(NOX_CMD + ('modify -name:{0} -resolution:{1},{2},{3} -cpu:{4} -memory:{5}').format(name,res1,re2,res3,cpu,mem))

def launchNox(name):
    return subprocess.call(NOX_CMD + ('launch -name:{0}').format(name))

def closeNox(name):
    return subprocess.call(NOX_CMD + ('quit -name:{0}').format(name))

def startNewNox(i):
    createNox(('NoxPlayer{}').format(i))
    modifyNox(('NoxPlayer{}').format(i),300,400,120,2,2048)
    launchNox(('NoxPlayer{}').format(i))

def closeNewNox(i):
    closeNox(('NoxPlayer{}'.format(i)))
    removeNox(i)

LD_CMD = r'G:\Download\LDPlayer\ldconsole.exe '

def createLD(name):
    return subprocess.call(LD_CMD + ('add --name {0}').format(name),shell=True)

def removeLD(name):
    return subprocess.call(LD_CMD + ('remove --name {}').format(name),shell=True)

def modify(name, res1, re2, res3, cpu, mem):
    return subprocess.call(LD_CMD + ('modify --name {0} --resolution {1},{2},{3} --cpu {4} --memory {5}').format(name,res1,re2,res3,cpu,mem),shell=True)

def launchLD(name):
    return subprocess.call(LD_CMD + ('launch --name {0}').format(name),shell=True)

def startNewLD(i):
    createLD(('NoxPlayer{}').format(i))
    modify(('NoxPlayer{}').format(i),300,400,120,1,2048)
    launchLD(('NoxPlayer{}').format(i))

def closeNewLD(i):
    subprocess.run(LD_CMD + 'quit --index {}'.format(i))
    subprocess.run(LD_CMD + 'remove --index {}'.format(i))

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


def grant(package, permission,device):
    cmd = "pm grant " + package + permission
    return device.shell(cmd)


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

def getNumberCTN(api):

    param = "&apikey={0}&action=create-request&serviceId=1&count=1".format(api)
    get = requests.get("http://codetextnow.com/api.php",params=param)
    number = json.loads(get.text)['results']['data'][0]
    return number['sdt'], number['requestId']

def getOTPCTN(api,requestid):

    param = "&apikey={0}&action=data-request&requestId={1}".format(api,requestid)
    getCode = requests.get("http://codetextnow.com/api.php",params=param).json()
    otp = getCode['data'][0]['otp']
    return otp

def getMailCTN(api):

    param = "&apikey={0}&action=create-request&serviceId=3&count=1".format(api)
    get = requests.get("http://codetextnow.com/api.php",params=param)
    number = json.loads(get.text)['results']['data'][0]
    return number['email'], number['requestId']

def getOTPMailCTN(api,requestid):

    param = "&apikey={0}&action=data-request-tempmail&requestId={1}".format(api,requestid)
    getCode = requests.get("http://codetextnow.com/api.php",params=param).json()
    otp = getCode['data'][0]['otp']
    return otp

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

def get_hotmailDV(api):

    get = requests.get(('http://dongvanfb.com/api/buyaccount.php?apiKey={0}&type=1&amount=1').format(api)).json()
    account = str(get['accounts'])

    for i in range(len(account)):
        if account[i] == '|':
            mail = account[:i]
            password = account[i+1:]
    return mail, password

def get_code_hotmailDV(api,mail,password):

    get = requests.get(('http://fbvip.org/api/ordercode.php?apiKey={0}&type=1&user={1}&pass={2}').format(api,mail,password)).json()
    id = get['id']
    code = requests.get(('http://fbvip.org/api/getcode.php?apiKey=7b537fb6a4d5d1dafbd4750ecbf29f74&id={0}').format(id)).json()
    return code['code']

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

def NoxregFacebook(i):

    #subprocess.run('G:/An/python/tool/test_openNox.py {}'.format(i), shell=True)
    # while True:
    #     try:
    #         time.sleep(10)
    #         cmd = subprocess.run('adb shell input tap 1 1').returncode
    #         if not cmd:
    #             break
    #     except:
    #         print('Chưa chạy')
    #time.sleep(40)
    file_1 = open(ho, "r", encoding="utf8").readlines()
    file_2 = open(ten, "r", encoding="utf8").readlines()

    device = getDevice(i)
    print("Đang nhập proxy")

    proxy = get_new_proxyTM('c86fbeaca7eb5a4b2fb07d3697410bab')

    if proxy == '':
        proxy = get_current_proxyTM('c86fbeaca7eb5a4b2fb07d3697410bab')

    device.shell(("settings put global http_proxy {}").format(proxy))
    #time.sleep(1)
    #print('Đang uninstall facebook')
    #device.uninstall('com.facebook.katana')
    #time.sleep(1)
    #
    #print('Đang install facebooklite')
    #device.install('apps/facebook.apk')
    #time.sleep(1)

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
    print("Nhấn Tạo tài khoản...")
    click_ocr("image/create.PNG",device)

    time.sleep(30)
    print("Nhấn Next...")
    click_ocr("image/next.PNG",device)
    time.sleep(2)

    # Cần đọc vào file
    print("Đang nhập họ và tên")
    time.sleep(random.randint(1,2))
    write_vn(file_1[random.randint(0,1375)],device)

    device.input_tap(177,188)
    write_vn(file_2[random.randint(0,212)],device)
    time.sleep(random.randint(1,2))

    print("Nhấn next")
    click_ocr("image/next.PNG",device)
    time.sleep(random.randint(1,2))

    # Nghiên cứu codetextnow hoặc tempmail

    print("Điền ngày tháng năm...")
    time.sleep(random.randint(1,2))
    print("Next lần 1...")
    click_ocr("image/next.PNG",device)

    time.sleep(random.randint(1,2))
    print("Next lần 2...")
    click_ocr("image/next.PNG",device)
    time.sleep(random.randint(1,2))

    device.input_tap(146, 146)
    time.sleep(random.randint(1,2))
    write_vn(str(random.randint(18,50)),device)
    time.sleep(random.randint(1,2))
    click_ocr("image/next.PNG",device)
    time.sleep(random.randint(1,2))

    click_ocr("image/ok2.PNG",device)

    time.sleep(2)
    print("Điền giới tính")
    click_ocr("image/gender.PNG",device)
    time.sleep(random.randint(1,2))
    click_ocr("image/next.PNG",device)
    time.sleep(random.randint(1,2))

    print("Đang điền số điện thoại")
    clear_input(13,device)
    time.sleep(random.randint(1,2))
    #click_ocr("image/reg_by_mail.PNG", device)
    #time.sleep(random.randint(1,2))

    number, id = get_number_VOTP('fd66a0ef1d8645ddbc5e0e5921d9b523')
    write_vn('+84' + number,device)
    time.sleep(random.randint(1,2))
    click_ocr('image/next.PNG',device)

    time.sleep(random.randint(1,2))
    print("Nhập password")
    passwd = password()
    write_vn(passwd, device)
    time.sleep(random.randint(1,2))
    click_ocr("image/next.PNG",device)
    time.sleep(random.randint(1,2))

    print("Đang tạo tài khoản")
    click_ocr("image/regist.PNG",device)
    time.sleep(25)

    click_ocr('image/other.PNG',device)
    time.sleep(random.randint(1,2))
    click_ocr('image/ok.PNG',device)
    time.sleep(random.randint(1,2))

    while True:
        time.sleep(random.randint(1,2))
        otp = get_otp_VOTP('fd66a0ef1d8645ddbc5e0e5921d9b523',id)
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
    #closeNew(i+1)

def LDregFacebook(i):

    startNewLD(i)

    time.sleep(40)
    file_1 = open(ho, "r", encoding="utf8").readlines()
    file_2 = open(ten, "r", encoding="utf8").readlines()

    device = getDevice(i)
    print("Đang nhập proxy")

    proxy = get_new_proxyTM('c86fbeaca7eb5a4b2fb07d3697410bab')

    if proxy == '':
        proxy = get_current_proxyTM('c86fbeaca7eb5a4b2fb07d3697410bab')

    device.shell(("settings put global http_proxy {}").format(proxy))
    #time.sleep(1)
    #print('Đang uninstall facebook')
    #device.uninstall('com.facebook.katana')
    #time.sleep(1)
    #
    #print('Đang install facebooklite')
    #device.install('apps/facebook.apk')
    #time.sleep(1)

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
    print("Nhấn Tạo tài khoản...")
    click_ocr("image/create.PNG",device)

    time.sleep(30)
    print("Nhấn Next...")
    click_ocr("image/next.PNG",device)
    time.sleep(2)

    # Cần đọc vào file
    print("Đang nhập họ và tên")
    time.sleep(random.randint(1,2))
    write_vn(file_1[random.randint(0,1375)],device)

    device.input_tap(177,188)
    write_vn(file_2[random.randint(0,212)],device)
    time.sleep(random.randint(1,2))

    print("Nhấn next")
    click_ocr("image/next.PNG",device)
    time.sleep(random.randint(1,2))

    # Nghiên cứu codetextnow hoặc tempmail

    print("Điền ngày tháng năm...")
    time.sleep(random.randint(1,2))
    print("Next lần 1...")
    click_ocr("image/next.PNG",device)

    time.sleep(random.randint(1,2))
    print("Next lần 2...")
    click_ocr("image/next.PNG",device)
    time.sleep(random.randint(1,2))

    device.input_tap(146, 146)
    time.sleep(random.randint(1,2))
    write_vn(str(random.randint(18,50)),device)
    time.sleep(random.randint(1,2))
    click_ocr("image/next.PNG",device)
    time.sleep(random.randint(1,2))

    click_ocr("image/ok2.PNG",device)

    time.sleep(2)
    print("Điền giới tính")
    click_ocr("image/gender.PNG",device)
    time.sleep(random.randint(1,2))
    click_ocr("image/next.PNG",device)
    time.sleep(random.randint(1,2))

    print("Đang điền số điện thoại")
    clear_input(13,device)
    time.sleep(random.randint(1,2))
    #click_ocr("image/reg_by_mail.PNG", device)
    #time.sleep(random.randint(1,2))

    number, id = get_number_VOTP('fd66a0ef1d8645ddbc5e0e5921d9b523')
    write_vn('+84' + number,device)
    time.sleep(random.randint(1,2))
    click_ocr('image/next.PNG',device)

    time.sleep(random.randint(1,2))
    print("Nhập password")
    passwd = password()
    write_vn(passwd, device)
    time.sleep(random.randint(1,2))
    click_ocr("image/next.PNG",device)
    time.sleep(random.randint(1,2))

    print("Đang tạo tài khoản")
    click_ocr("image/regist.PNG",device)
    time.sleep(25)

    click_ocr('image/other.PNG',device)
    time.sleep(random.randint(1,2))
    click_ocr('image/ok.PNG',device)
    time.sleep(random.randint(1,2))

    while True:
        time.sleep(random.randint(1,2))
        otp = get_otp_VOTP('fd66a0ef1d8645ddbc5e0e5921d9b523',id)
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
    #closeNew(i+1)

for i in range(thread_num):
    t0 = threading.Thread(target=NoxregFacebook, args=(0,))
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

